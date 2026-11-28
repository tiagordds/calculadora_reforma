import json
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlencode

import pytest
from django.core.management import CommandError, call_command
from django.test import Client

from parameters import retail, services
from parameters.catalog import CatalogError
from simulation.mixed import EDITION

URL = "/simples/atividades-mistas/"
MONTHS = tuple(f"2026-{month:02}" for month in range(2, 13)) + ("2027-01",)
EVIDENCE = Path(__file__).resolve().parents[1] / "docs/evidencias/mistas01"


@pytest.fixture
def inputs():
    data = dict(edition=EDITION, period="2027-03", opening="2023-01", activity="mixed", regime="traditional",
                retail_treatment="ordinary", service_treatment="ordinary", limits="within", origin="synthetic",
                retail="60000", service="40000")
    for month in MONTHS:
        for key, value in dict(retail="60000", service="40000", wages="20000", pro_labore="5000",
                               cpp="2000", fgts="1000", origin="synthetic").items():
            data[f"{key}_{month}"] = value
    return data


def post(client, data):
    return client.post(URL, urlencode(data, doseq=True), content_type="application/x-www-form-urlencoded")


@pytest.mark.parametrize("pay,annex,rate,service,total,allocation,residue", [
    ("19999.99", "V", "19.075", 7630, 12925, "1893.53 1329.83 2256.85 4043.66 1773.83 1602.30 25.02", ".02"),
    ("20000", "III", "13.03", 5212, 10507, "499.71 367.75 1667.01 4485.91 1773.83 1693.90 18.90", ".01"),
    ("20000.01", "III", "13.03", 5212, 10507, "499.71 367.75 1667.01 4485.91 1773.83 1693.90 18.90", ".01"),
])
def test_independent_dou_references(client, inputs, pay, annex, rate, service, total, allocation, residue):
    response = post(client, dict(inputs, **{"wages_2027-01": pay}))
    assert response.status_code == 200
    m = response.context["memory"]
    assert m["revenue"] == 100000 and m["history"]["months"] == MONTHS
    assert m["history"]["fs12"] == Decimal(pay) + 316000
    assert m["history"]["rbt12r"] == m["rate_basis"] == 1200000
    trade, software = m["groups"]
    assert trade["annex"] == "I" and software["annex"] == m["factor"]["annex"] == annex
    assert trade["band"]["number"] == software["band"]["number"] == 4
    assert trade["amounts"]["effective_percent"] == Decimal("8.825")
    assert software["amounts"]["effective_percent"] == Decimal(rate)
    assert (trade["amounts"]["gross"], software["amounts"]["gross"], m["amounts"]["gross"]) == (5295, service, total)
    assert "ISS" not in trade["band"]["shares"] and "ICMS" not in software["band"]["shares"]
    rows = m["amounts"]["rows"]
    assert len(rows) == 7
    assert {row["tax"]: row["displayed"] for row in rows} == dict(zip(
        "IRPJ CSLL CBS CPP ICMS ISS IBS".split(), map(Decimal, allocation.split())))
    assert sum(row["exact"] for row in rows) == total
    assert m["amounts"]["residue"] == Decimal(residue) and m["amounts"]["activity_residue"] == 0
    assert m["guide"] is None and m["engines"] == []


def test_different_months_and_mix(client, inputs):
    inputs.update(retail="20000", service="80000")
    inputs.update({"retail_2026-02": "20000", "service_2026-03": "80000", "origin_2026-02": "estimated",
                   "origin_2026-03": "entered"})
    m = post(client, inputs).context["memory"]
    series = m["history"]["series"]
    assert [(series[k]["turnover"], series[k]["origin"]) for k in MONTHS[:2]] == [
        (60000, "estimated"), (140000, "entered")]
    assert m["rate_basis"] == 1200000 and m["amounts"]["monthly"] == 1765 + 10424


@pytest.mark.parametrize("group,other,known", [("retail", 1, 5212), ("service", 0, 5295)])
def test_zero_and_missing_current(client, inputs, group, other, known):
    m = post(client, dict(inputs, **{group: "0"})).context["memory"]
    assert m["amounts"]["monthly"] == known and m["rate_basis"] == 1200000
    m = post(client, dict(inputs, **{group: ""})).context["memory"]
    assert m["revenue"] is None and "amounts" not in m
    assert "amounts" not in m["groups"][1-other]
    assert m["groups"][other]["amounts"]["monthly"] == known


@pytest.mark.parametrize("key", ["retail", "service", "wages", "pro_labore", "cpp", "fgts"])
def test_history_gap(client, inputs, key):
    inputs[f"{key}_2027-01"] = ""
    response = post(client, inputs)
    m = response.context["memory"]
    assert m["factor"] is None and "amounts" not in m
    assert m["history"]["series"]["2027-01"]["missing"] == [key]
    assert f"{key}_2027-01" in response.content.decode()
    if key in ("retail", "service"):
        assert m["rate_basis"] is None and m["history"]["fs12"] == 336000
        assert all("amounts" not in group for group in m["groups"])
    else:
        assert m["history"]["fs12"] is None and m["groups"][0]["amounts"]["gross"] == 5295


@pytest.mark.parametrize("monthly,expected,nominal,cpp", [
    ("0", 1, "4", "41.5"), ("15000", 1, "4", "41.5"), ("15000.01", 2, "7.3", "41.5"),
    ("30000.01", 3, "9.5", "42"), ("60000.01", 4, "10.7", "42"), ("150000.01", 5, "14.3", "42")])
def test_retail_table_and_zero_history(client, inputs, monthly, expected, nominal, cpp):
    for month in MONTHS:
        inputs[f"retail_{month}"] = monthly
        inputs[f"service_{month}"] = "0"
    m = post(client, inputs).context["memory"]
    band = m["groups"][0]["band"]
    assert band["number"] == expected and Decimal(band["nominal"]) == Decimal(nominal)
    assert Decimal(band["shares"]["CPP"]) == Decimal(cpp)
    assert sum(map(Decimal, band["shares"].values())) == 100
    assert "amounts" in m
    if monthly == "0":
        assert m["rate_basis"] == 1 and m["factor"]["ratio"] == Decimal(".28")


def test_iss_cap_and_company_allocation(client, inputs):
    for month in MONTHS:
        inputs[f"retail_{month}"] = "210000"
        inputs[f"wages_{month}"] = "70000"
    m = post(client, inputs).context["memory"]
    assert m["groups"][1]["amounts"]["iss_capped"]
    rows = {r["tax"]: r["exact"] for r in m["amounts"]["rows"]}
    assert rows["ISS"] == 2000 and m["groups"][0]["band"]["number"] == 5
    assert sum(rows.values()) == m["amounts"]["gross"]


def test_known_zero_payroll(client, inputs):
    for month in MONTHS:
        for component in ("wages", "pro_labore", "cpp", "fgts"):
            inputs[f"{component}_{month}"] = "0"
    m = post(client, inputs).context["memory"]
    assert m["history"]["fs12"] == 0 and m["factor"]["ratio"] == Decimal(".01")
    assert m["groups"][1]["annex"] == "V" and m["amounts"]["monthly"] == 12925


def test_subcent_consolidation(client, inputs):
    m = post(client, dict(inputs, retail="0.01", service="0.01")).context["memory"]
    assert m["amounts"]["gross"] == Decimal(".0021855")
    assert m["amounts"]["monthly"] == Decimal(".01")
    assert m["amounts"]["activity_residue"] == Decimal(".01") and m["amounts"]["residue"] == Decimal(".06")


@pytest.mark.parametrize("changes,words", [
    ({"limits": "unknown"}, "limite anual"), ({"limits": "excess"}, "Excesso"),
    ({"retail": "3500000.01", "service": ""}, "Excesso"), ({"retail_2026-02": "3600000.01", "service_2026-02": ""}, "Excesso"),
    ({"opening": "2026-02", "retail_2026-02": "2260000.01"}, "Excesso"),
    ({"period": "2027-04"}, "competência"), ({"opening": "2026-03"}, "14º mês"),
    ({"regime": "other"}, "tradicional"), ({"activity": "other"}, "sem outras atividades"),
])
def test_enterprise_blocks(client, inputs, changes, words):
    m = post(client, inputs | changes).context["memory"]
    assert words in " ".join(m["reasons"])
    assert "amounts" not in m and all("amounts" not in group for group in m.get("groups", []))


def test_sixth_band_even_if_reported_years_within_limit(client, inputs):
    for month in MONTHS:
        inputs[f"retail_{month}"] = "260000.01"
    m = post(client, inputs).context["memory"]
    assert m["history"]["rbt12r"] > 3600000 and m["groups"][1]["band"]["number"] == 6
    assert all("cinco faixas" in group["reasons"][0] for group in m["groups"])
    assert "amounts" not in m


@pytest.mark.parametrize("index,key", [(0, "retail_treatment"), (1, "service_treatment")])
def test_special_treatment_is_local(client, inputs, index, key):
    m = post(client, dict(inputs, **{key: "special"})).context["memory"]
    assert m["groups"][index]["reasons"] and "amounts" not in m["groups"][index]
    assert "amounts" in m["groups"][1-index] and "amounts" not in m


@pytest.mark.parametrize("changes", [{"retail": ["1", "2"]}, {"service_2026-02": ["0", "0"]},
    {"service": "-1"}, {"service": "NaN"}, {"retail": "1,001"}, {"other": "0"}, {"retail_2027-02": "0"},
    {"opening": "2027-04"}, {"edition": "old"}, {"example": ["c09", "c09"]}, {"origin_2026-02": "invalid"}])
def test_invalid_and_retained(client, inputs, changes):
    response = post(client, inputs | changes)
    assert response.status_code == 400 and response.context["memory"] is None
    assert response.context["form"]["wages_2027-01"].value() == "20000"


def test_private_form_and_csrf(client, inputs):
    assert URL in client.get("/").content.decode()
    page = client.get(URL)
    assert "no-store" in page["Cache-Control"] and "noindex" in page["X-Robots-Tag"]
    assert client.get(URL + "?service=1").status_code == 400
    assert post(Client(enforce_csrf_checks=True), inputs).status_code == 403
    example = post(client, {"example": "c09"}).context["form"]
    assert example["retail"].value() == "60000" and example["service_2027-01"].value() == "40000"


@pytest.mark.parametrize("module,loader,index", [(services, "load_rules", 1), (retail, "load_retail", 0)])
def test_unavailable_keeps_other_result(client, inputs, monkeypatch, module, loader, index):
    def unavailable(*args):
        raise CatalogError("Revisão indisponível.")
    monkeypatch.setattr(module, loader, unavailable)
    response = post(client, inputs)
    m = response.context["memory"]
    assert response.status_code == 503 and "amounts" not in m
    assert "amounts" not in m["groups"][index] and "amounts" in m["groups"][1-index]


@pytest.mark.parametrize("annex", ["iii", "v"])
def test_archived_replay(annex):
    call_command("replay_mixed", EVIDENCE / f"c09-{annex}.json")


def test_partial_replay_and_parameter_tampering(client, inputs, tmp_path):
    data = json.loads(post(client, dict(inputs, service="")).context["replay"])
    file = tmp_path / "partial.json"
    file.write_text(json.dumps(data), encoding="utf-8")
    call_command("replay_mixed", file)
    data["editions"]["sn-services-01"] = "changed"
    file.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(CommandError, match="divergiu"):
        call_command("replay_mixed", file)
