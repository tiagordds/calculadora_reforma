import json
from datetime import date
from decimal import Decimal as D
from pathlib import Path
from urllib.parse import urlencode

import pytest
from django.core.management import CommandError, call_command
from django.http import QueryDict
from django.test import Client

from parameters import comparison as edition
from parameters.catalog import CatalogError
from simulation.service_comparison import compare_services
from tax.option import window
from web.service_comparison import ServiceComparisonForm, sample

URL = "/simples/servicos/comparar/"
CENT = D(".01")
MARCH = date(2027, 3, 1)
ARCHIVE = Path(__file__).resolve().parents[1] / "docs/evidencias"


def scenario(**changes):
    post = QueryDict(mutable=True)
    post.update(dict(sample(), **changes))
    form = ServiceComparisonForm(post)
    assert form.is_valid(), form.errors
    return compare_services(form.scenario())


def submit(client, fields):
    return client.post(URL, urlencode(fields, doseq=True), content_type="application/x-www-form-urlencoded")


@pytest.mark.parametrize("traditional_wage,hybrid_wage,hybrid_january,expected", [
    ("20000", "20000", "100000", ("III", "III")),
    ("19999.99", "19999.99", "100000", ("V", "V")),
    ("19999.99", "19999.99", "90000", ("V", "III")),
    ("20000", "19999.99", "100000", ("III", "V")),
    ("20000", "20000", "100000.01", ("III", "V")),
])
def test_independent_histories(traditional_wage, hybrid_wage, hybrid_january, expected):
    m = scenario(**{"wages_2027-01": traditional_wage, "hybrid_wages_2027-01": hybrid_wage,
                    "hybrid_turnover_2027-01": hybrid_january})
    a, b = m["traditional"], m["hybrid"]
    assert (a["factor"]["annex"], b["factor"]["annex"]) == expected
    assert a["history"]["fs12"] == 316000 + D(traditional_wage)
    assert b["history"]["fs12"] == 316000 + D(hybrid_wage)
    assert b["history"]["rbt12r"] == 1100000 + D(hybrid_january)
    assert a["basis"] == b["basis"] and a["basis"]["quantity"] == 10
    assert a["revenue"] == 100000 and b["revenue"] < a["revenue"]
    assert m["difference"] is not None


@pytest.mark.parametrize("annex,wage,effective,iss,retained", [
    ("III", "20000", "0.1303", "0.325", "0.834"),
    ("V", "19999.99", "0.19075", "0.21", "0.8085")])
def test_direct_algebra_from_official_fourth_band(annex, wage, effective, iss, retained):
    b = scenario(**{"hybrid_wages_2027-01": wage, "hybrid_turnover_2027-01": "100000"})["hybrid"]
    # Independent derivation: H = P / (1 + (1 - effective ISS) * 0.101).
    h = D(100000) / (1 + (1 - D(effective) * D(iss)) * D(".101"))
    base = h * (1 - D(effective) * D(iss))
    assert b["factor"]["annex"] == annex
    rows = {r["tax"]: r["exact"] for r in b["das"]["rows"]}
    assert set(rows) == {"ISS", "CPP", "IRPJ", "CSLL"}
    for actual, expected in ((rows["ISS"], h*D(effective)*D(iss)),
                             (b["das"]["exact"], h*D(effective)*D(retained)),
                             (b["regular"]["cbs"], base/10),
                             (b["regular"]["state"], base*D(".0005")),
                             (b["regular"]["city"], base*D(".0005")),
                             (b["regular"]["base"], base)):
        assert abs(actual - expected) < D("1e-20")
    assert (h + b["regular"]["debit"]).quantize(CENT) == 100000


@pytest.mark.parametrize("field", ["hybrid_wages_2026-03", "hybrid_turnover_2027-01"])
def test_unknown_history_preserves_documented_debits(field):
    m = scenario(iss_basis="document", iss_amount="3900", **{field: ""})
    b = m["hybrid"]
    assert "factor" not in b and b["das"] is None
    assert b["regular"]["base"].quantize(CENT) == (D(96100)/D("1.101")).quantize(CENT)
    assert m["traditional"]["das"] and m["difference"] is None


def test_hybrid_iss_cap_before_removing_regular_shares():
    months = [f"2026-{m:02}" for m in range(2, 13)] + ["2027-01"]
    fields = {f"hybrid_turnover_{m}": "250000" for m in months}
    fields.update({f"hybrid_wages_{m}": "75000" for m in months})
    hybrid = scenario(**fields)["hybrid"]
    assert hybrid["das"]["iss_capped"] and hybrid["regular"]["iss_share"] == D(".05")
    effective = D(".05") + D(".11812") * (1 - D(".2320") - D(".0026"))
    assert abs(hybrid["das"]["exact"] - hybrid["revenue"] * effective) < D("1e-20")


def test_credit_states_and_separate_excess():
    missing = scenario(cbs_credit="")["hybrid"]
    assert missing["gross"] is not None and missing["net"] is None
    assert missing["accounts"]["ibs"]["appropriated"] == 0
    high = scenario(cbs_credit="9500", ibs_credit="20")["hybrid"]
    assert high["accounts"]["cbs"]["closing"].quantize(CENT) == D("767.38")
    assert high["accounts"]["ibs"]["net"].quantize(CENT) == D("67.33")
    assert high["accounts"]["ibs"]["closing"] == 0
    assert scenario(event_month="2027-04", cbs_credit="20")["hybrid"]["accounts"]["cbs"]["appropriated"] == 0
    assert scenario(credit_evidence="", cbs_credit="20")["difference"] is None


@pytest.mark.parametrize("changes", [
    {"accept_cbs": ""}, {"iss_basis": "unknown"}, {"exclusion_origin": "unknown"},
    {"option_status": "absent", "option_date": ""}, {"option_status": "unknown", "option_date": ""},
    {"cancel_date": "2026-12-20"}, {"destination": "unknown"}, {"account_scope": ""},
    {"refund": "yes"}, {"credit_origin": "unknown"}])
def test_partial_preserves_traditional(changes):
    m = scenario(**changes)
    assert m["traditional"]["das"]["displayed"] == 19075 and m["difference"] is None
    if changes.get("option_status") == "absent" or "cancel_date" in changes:
        assert m["hybrid"]["gross"] is None and m["hybrid"]["accounts"] == {}


def test_known_turnover_separates_ibs_from_unknown_cbs():
    b = scenario(hybrid_revenue="91000", iss_basis="document", iss_amount="3900", accept_cbs="")["hybrid"]
    assert b["das"] and b["revenue"] == 91000
    assert b["regular"]["base"] == 87100 and b["regular"]["ibs"] == D("87.10")
    assert b["regular"]["cbs"] is None and b["net"] is None
    mismatch = scenario(hybrid_revenue="91000", iss_basis="document", iss_amount="3900")
    assert mismatch["difference"] is None and mismatch["hybrid"]["regular"]["issue"]


def test_shared_history_requires_choice(client):
    d = {k: v for k, v in sample().items() if not k.startswith("hybrid_")}
    d["history_basis"] = "shared"
    m = submit(client, d).context["memory"]
    assert m["traditional"]["history"] == m["hybrid"]["history"]
    assert m["hybrid"]["history_origin"] == "shared" and m["conditions"]
    assert submit(client, dict(sample(), history_basis="shared")).status_code == 400


@pytest.mark.parametrize("changes", [{"period": "2026-12"}, {"period": "2028-03", "event_month": ""}, {"activity": "other"},
                                     {"regime": "other"}, {"opening": "2027-03"}, {"destination": "public"}])
def test_qualified_period_and_profile(changes):
    m = scenario(**changes)
    assert m["difference"] is None and m["traditional"]["das"] is None and m["hybrid"]["das"] is None


def test_documentary_and_engine_limits(monkeypatch):
    def unexpected(*args, **kwargs):
        pytest.fail("O C08 tentou consultar o motor documental.")
    monkeypatch.setattr("adapters.regular.call", unexpected)
    m = scenario()
    assert m["engines"] == [] and "sem combinação qualificada" in m["document"] and "C16" in m["document"]
    assert m["difference"] and m["payment"] is None
    monkeypatch.setattr(edition, "regular_rules", lambda *a: (_ for _ in ()).throw(CatalogError("indisponível")))
    partial = scenario()
    assert partial["traditional"]["das"] and partial["difference"] is None
    assert partial["states"]["technical"] == "Parâmetros indisponíveis"


@pytest.mark.parametrize("name", ["fronteira", "credito-pendente"])
def test_saved_service_comparison(name):
    call_command("replay_service_comparison", ARCHIVE / "servicos-hibrido01" / (name + ".json"))


def test_ordinary_calendar_is_versioned():
    old = edition.regular_rules(MARCH, edition.PREVIOUS)
    new = edition.regular_rules(MARCH)
    for month, cancel_month in ((3, 5), (9, 11)):
        day = date(2027, month, 15)
        assert window(day, old)[1][0] == day
        assert window(day, new)[1][0] == date(2027, cancel_month, 1)
    assert window(date(2026, 10, 30), new) == window(date(2026, 10, 30), old)


@pytest.mark.parametrize("key,value", [("accept_cbs", "false"), ("revenue", ["1", "2"]),
    ("iss_amount", "29000"), ("cbs_credit", "-2"), ("extra", "x"), ("quantity", "0"),
    ("cbs_rate", "101"), ("period", "2027-17"), ("hybrid_revenue", "100001")])
def test_invalid_posts_preserve_input(client, key, value):
    r = submit(client, dict(sample(), **{key: value}))
    assert r.status_code == 400 and r.context["memory"] is None
    assert r.context["form"]["wages_2027-01"].value() == "19999.99"


def test_form_security_carry_and_replay(tmp_path):
    c = Client(enforce_csrf_checks=True)
    token = c.get(URL).cookies["csrftoken"].value
    assert submit(c, sample()).status_code == 403
    assert c.get(URL + "?valor=1").status_code == 400
    assert submit(c, {"example": ["boundary", "boundary"], "csrfmiddlewaretoken": token}).status_code == 400
    r = submit(c, dict(sample(), csrfmiddlewaretoken=token))
    assert "no-store" in r["Cache-Control"] and "anexos diferentes" in r.content.decode()
    file = tmp_path / "c08.json"
    file.write_text(r.context["replay"], encoding="utf8")
    call_command("replay_service_comparison", file)
    m = json.loads(file.read_bytes())
    m["hybrid"]["revenue"] = "0"
    file.write_text(json.dumps(m), encoding="utf8")
    with pytest.raises(CommandError):
        call_command("replay_service_comparison", file)
    from web.services import flatten_history, example_inputs
    carried = submit(c, dict(flatten_history(example_inputs()), edition="sn-services-01",
                             carry="services", csrfmiddlewaretoken=token))
    assert carried.status_code == 200 and carried.context["form"]["turnover_2027-01"].value() == "100000"


@pytest.mark.parametrize("name", ["zero", "middle", "high"])
@pytest.mark.parametrize("phase", ["04", "05"])
def test_archived_calendar_and_money(name, phase):
    call_command("replay_comparison", ARCHIVE / phase / (name + ".json"))
