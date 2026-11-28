import json
from decimal import Decimal as D
from pathlib import Path
from urllib.parse import urlencode

import pytest
from django.core.management import CommandError, call_command
from django.http import QueryDict
from django.test import Client

from parameters import comparison
from parameters.catalog import CatalogError
from simulation.mixed_comparison import compare_mixed
from web.mixed_comparison import MixedComparisonForm, sample

URL = "/simples/atividades-mistas/comparar/"
EVIDENCE = Path(__file__).resolve().parents[1] / "docs/evidencias/mistas-hibrido01"
CENT = D(".01")


def form_for(fields):
    post = QueryDict(mutable=True)
    post.update(fields)
    return MixedComparisonForm(post)


def scenario(**changes):
    form = form_for(sample() | changes)
    assert form.is_valid(), form.errors
    return compare_mixed(form.scenario())


def submit(client, data):
    return client.post(URL, urlencode(data, doseq=True), content_type="application/x-www-form-urlencoded")


def test_two_business_bases_and_dou_reference():
    memory = scenario()
    a, b = memory["traditional"], memory["hybrid"]
    assert a["history"]["rbt12r"] == 1200000 and b["history"]["rbt12r"] == 1190000
    assert a["history"]["fs12"] == b["history"]["fs12"] == D("335999.99")
    assert b["history"]["series"]["2027-01"]["turnover"] == 90000
    assert b["history"]["months"][0] == "2026-02" and b["history"]["months"][-1] == "2027-01"
    assert a["amounts"]["gross"] == 12925 and a["revenue"] == 100000
    trade, service = b["groups"]
    # (P − ICMS/ISS − other exclusions) = B × 1.101. DOU tables I and III, fourth band.
    for row, base, revenue, portion, local_tax in (
            (trade, 50000, 54950, D(54950) * (D(".107") - D(22500)/1190000) * D(".845"), "ICMS"),
            (service, 35000, 36465, D(36465) * (D(".16") - D(35640)/1190000) * D(".834"), "ISS")):
        r = row["regular"]
        assert row["revenue"] == revenue and r["base"] == base
        assert r["state"] == r["city"] == base * D(".0005") and r["cbs"] == base / 10
        assert row["das"]["displayed"] == portion.quantize(CENT)
        assert {item["tax"] for item in row["das"]["rows"]} == {"IRPJ", "CSLL", "CPP", local_tax}
        assert {item["tax"] for item in row["excluded_rows"]} == {"IBS", "CBS"}
    assert trade["regular"]["icms"] == 4950 and service["regular"]["iss_excluded"] == 1463
    assert b["revenue"] == 91415 and b["das"]["monthly"] == D("8045.44")
    assert b["accounts"]["cbs"]["debit"] == 8500 and b["accounts"]["ibs"]["debit"] == 85
    assert b["net"].quantize(CENT) == D("16630.44") and memory["difference"]["amount"].quantize(CENT) == D("3705.44")
    assert memory["engines"] == [] and memory["guide"] is memory["cash"] is memory["margin"] is None


@pytest.mark.parametrize("wage,hybrid_wage,annex,other", [
    ("19999.99", "17199.99", "V", "V"), ("19999.99", "17200", "V", "III"),
    ("20000", "17199.99", "III", "V"), ("20000", "17200", "III", "III")])
def test_exact_enterprise_payroll_boundary(wage, hybrid_wage, annex, other):
    m = scenario(**{"wages_2027-01": wage, "hybrid_wages_2027-01": hybrid_wage})
    for path, expected in ((m["traditional"], annex), (m["hybrid"], other)):
        assert path["factor"]["annex"] == expected
        assert [group["annex"] for group in path["groups"]] == ["I", expected]
        if expected == "III":
            assert path["factor"]["percent"] == 28
    assert m["difference"] is not None


@pytest.mark.parametrize("field,group", [("retail_extra", 0), ("icms", 0), ("service_extra", 1),
                                        ("iss_amount", 1), ("service", 1), ("retail", 0)])
def test_incomplete_group_preserves_independent_group(field, group):
    m = scenario(**{field: ""})
    b = m["hybrid"]
    assert b["groups"][group]["regular"]["debit"] is None
    assert b["groups"][1-group]["regular"]["debit"] == (3535, 5050)[group]
    assert "das" in b["groups"][1-group] and b["das"] is None and b["net"] is None
    assert b["accounts"]["cbs"]["debit"] is None and m["difference"] is None
    if field in ("retail", "service"):
        assert "amounts" not in m["traditional"]
        assert "amounts" in m["traditional"]["groups"][1-group]
    else:
        assert m["traditional"]["amounts"]["monthly"] == 12925


def test_pending_rate_reconciled_service_and_missing_history():
    m = scenario(cbs_rate="", service_reported="36465")
    trade, service = m["hybrid"]["groups"]
    assert trade["regular"]["revenue"] is None and service["regular"]["base"] == 35000
    assert service["regular"]["ibs"] == 35 and service["regular"]["cbs"] is None
    assert service["das"]["displayed"] == D("3955.07") and m["difference"] is None
    assert scenario(accept_cbs="")["hybrid"]["net"] is None
    m = scenario(**{"hybrid_fgts_2026-09": ""})
    assert m["hybrid"]["history"]["series"]["2026-09"]["missing"] == ["fgts"]
    assert m["hybrid"]["groups"][0]["das"] and m["hybrid"]["accounts"]["cbs"]["net"] == 8500
    m = scenario(**{"hybrid_service_2026-09": ""})
    assert m["hybrid"]["history"]["rbt12r"] is None and m["hybrid"]["das"] is None
    assert m["traditional"]["amounts"]["monthly"] == 12925


def test_shared_history_requires_explicit_choice():
    fields = sample()
    for key in list(fields):
        if key.startswith("hybrid_") and not key.startswith("hybrid_origin_"):
            fields[key] = ""
    own = scenario(**fields)
    assert own["hybrid"]["history"]["rbt12r"] is None and own["difference"] is None
    shared = scenario(**(fields | {"history_basis": "shared"}))
    assert shared["traditional"]["history"] == shared["hybrid"]["history"]
    assert shared["hybrid"]["factor"]["annex"] == "V" and shared["difference"] is not None


def test_proportional_iss_and_different_hybrid_band():
    changes = dict(iss_basis="proportional", iss_amount="")
    for month in scenario()["traditional"]["history"]["months"]:
        changes.update({f"hybrid_retail_{month}": "150000", f"hybrid_service_{month}": "100000",
                        f"hybrid_wages_{month}": "75000"})
    m = scenario(**changes)
    h = m["hybrid"]["groups"][1]
    assert m["traditional"]["groups"][0]["band"]["number"] == 4
    assert m["hybrid"]["groups"][0]["band"]["number"] == h["band"]["number"] == 5
    assert h["iss_capped"] and h["regular"]["iss_share"] == D(".05")
    assert abs(h["regular"]["iss_excluded"] - h["revenue"]*D(".05")) < D("1e-22")
    assert abs(h["das"]["exact"] - h["revenue"]*(D(".05") + D(".11812") * D(".7654"))) < D("1e-21")
    assert m["difference"] is not None


def test_price_conflict_and_destination_only_block_service():
    for m in (scenario(service_reported="35999"), scenario(destination="unknown"), scenario(destination="other")):
        assert m["hybrid"]["groups"][1]["regular"]["debit"] is None and m["difference"] is None
        assert m["hybrid"]["groups"][0]["regular"]["debit"] == 5050
    assert "amounts" not in scenario(destination="public")["traditional"]["groups"][1]


def test_one_unknown_credit_and_unconfirmed_movements():
    m = scenario(**{"shared-cbs_credit": ""})
    b = m["hybrid"]
    assert b["gross"].quantize(CENT) == D("16630.44") and b["das"]["monthly"] == D("8045.44")
    assert b["accounts"]["cbs"]["net"] is None and b["accounts"]["ibs"]["net"] == 85
    assert b["net"] is m["difference"] is None
    for changes in ({"zero_movements": ""}, {"account_scope": ""}, {"shared-credit_evidence": ""}):
        assert scenario(**changes)["hybrid"]["net"] is None


def test_no_acquisitions_requires_declaration():
    fields = {k: v for k, v in sample().items() if not k.startswith("shared-")}
    f = form_for(fields)
    assert f.is_valid()
    assert compare_mixed(f.scenario())["hybrid"]["net"] is None
    f = form_for(fields | {"no_acquisitions": "on"})
    assert f.is_valid()
    assert compare_mixed(f.scenario())["hybrid"]["net"].quantize(CENT) == D("16630.44")


def test_shared_credit_counted_once_and_other_documents_consolidated():
    fields = sample()
    for prefix, cbs, ibs in (("retail", 220, 3), ("retail_1", 120, 2), ("service", 160, 5), ("shared", 8500, 100)):
        fields.update({f"{prefix}-{key.split('-')[1]}": v for key, v in sample().items() if key.startswith("shared-")})
        fields.update({f"{prefix}-document": prefix, f"{prefix}-cbs_credit": str(cbs), f"{prefix}-ibs_credit": str(ibs)})
    b = scenario(**fields)["hybrid"]
    assert b["accounts"]["cbs"]["appropriated"] == 9000 and b["accounts"]["ibs"]["appropriated"] == 110
    assert b["accounts"]["cbs"]["closing"] == 500 and b["accounts"]["ibs"]["closing"] == 25
    assert b["accounts"]["cbs"]["used"] == 8500 and b["accounts"]["ibs"]["used"] == 85
    assert b["net"] == b["das"]["gross"]
    b = scenario(**{"shared-ibs_credit": "185", "shared-cbs_credit": "10"})["hybrid"]
    assert b["accounts"]["ibs"]["closing"] == 100 and b["accounts"]["cbs"]["net"] == 8490


def test_event_transfer_and_residue():
    m = scenario(**{"shared-event_month": "2027-04", "shared-supplier": "simples", "shared-cbs_transfer": "400"})
    credit = m["hybrid"]["accounts"]["cbs"]["acquisitions"][0]
    assert credit["assessed"] == 400 and credit["appropriated"] == 0
    das = scenario(retail="59999.85", service="40001.07")["hybrid"]["das"]
    assert das["residue"] == sum(row["displayed"] for row in das["rows"]) - das["monthly"]
    assert das["residue"] or das["activity_residue"]


@pytest.mark.parametrize("changes,active", [
    ({"option_status": "unknown", "option_date": ""}, None), ({"option_status": "requested"}, None),
    ({"option_status": "assumed"}, None), ({"option_date": "2026-10-31"}, False),
    ({"option_status": "absent", "option_date": ""}, False), ({"option_date": "2027-03-05"}, False),
    ({"cancel_date": "2026-11-03"}, False), ({"refund": "yes"}, True), ({"fixed_basket": ""}, True)])
def test_no_global_conclusion_without_comparability(changes, active):
    m = scenario(**changes)
    assert m["option"]["active"] is active and m["traditional"]["amounts"]["gross"] == 12925
    assert m["difference"] is None and (m["hybrid"] is None) == (active is False)


@pytest.mark.parametrize("changes", [
    {"extra": "1"}, {"shared-extra": "1"}, {"edition": "mixed-01"}, {"fixed_basket": "yes"},
    {"retail_extra": "-2"}, {"retail": ["60000", "1"]}, {"shared-document": ["X", "X"]},
    {"history_basis": "shared"}, {"iss_amount": "41000"}, {"icms": "60001"},
    {"shared-event_month": "2027-02"}, {"no_acquisitions": "on"},
    {"shared-cbs_credit": "100", "shared-cbs_potential": "50"}, {"shared-credit_evidence": "talvez"},
    {"option_date": "9999-09-20"}, {"decision_date": "9999-09-20"}])
def test_form_rejects_invalid_and_ambiguous_fields(client, changes):
    r = submit(client, sample() | changes)
    assert r.status_code == 400 and r.context["memory"] is None
    assert r.context["form"]["service"].value() == "40000"


def test_duplicate_document_and_addition(client):
    fields = sample()
    fields.update({k.replace("shared-", "retail-"): v for k, v in sample().items() if k.startswith("shared-")})
    fields["retail-document"] = "exemplo-01"
    assert submit(client, fields).status_code == 400
    r = submit(client, sample() | {"add_purchase": "shared"})
    assert r.status_code == 200 and r.context["memory"] is None
    assert "shared_1" in r.context["form"].purchases


def test_private_journey_csrf_and_partial_catalog(client, monkeypatch):
    assert Client(enforce_csrf_checks=True).post(URL, {}, content_type="application/x-www-form-urlencoded").status_code == 403
    assert client.get(URL + "?dados=1").status_code == 400
    assert client.get(URL)["X-Robots-Tag"] == "noindex, nofollow"
    def unavailable(*args):
        raise CatalogError("Edição incompatível.")
    monkeypatch.setattr(comparison, "regular_rules", unavailable)
    r = submit(client, sample() | {"service_reported": "36465"})
    assert r.status_code == 503 and r.context["memory"]["traditional"]["amounts"]["monthly"] == 12925
    assert r.context["memory"]["hybrid"]["groups"][1]["das"]["displayed"] == D("3955.07")
    assert r.context["memory"]["difference"] is None


def test_archive_and_tamper(tmp_path):
    files = list(EVIDENCE.glob("*.json"))
    assert len(files) >= 5
    for file in files:
        call_command("replay_mixed_comparison", file)
    for key in ("inputs", "catalogs"):
        changed = json.loads(files[0].read_bytes())
        if key == "inputs":
            changed[key]["history"]["2027-01"]["retail"] = "1"
        else:
            changed[key]["comparison-04-02"] = "0" * 64
        file = tmp_path / "alterado.json"
        file.write_text(json.dumps(changed), encoding="utf-8")
        with pytest.raises(CommandError):
            call_command("replay_mixed_comparison", file)
