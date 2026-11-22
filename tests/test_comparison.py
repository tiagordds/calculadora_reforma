import json
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from datetime import date
from decimal import Decimal as D, localcontext
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import Client

from parameters import comparison as edition
from simulation.comparison import compare
from simulation.economics import differences
from tax.credits import AccountError, account, acquisition
from tax.option import election, window
from tax.traditional import CENT, POLICY, history_window
from web.comparison_form import ComparisonForm
from web.comparison_view import example_post
from web.templatetags.comparison import money

URL = "/simples/comparar/"
REFERENCE = json.loads((Path(__file__).resolve().parents[1] / "docs/evidencias/00b/reference.json").read_bytes())
MARCH, APRIL = date(2027, 3, 1), date(2027, 4, 1)


def scenario(case="middle", **changes):
    post = example_post(case)
    for name, value in changes.items():
        post[name] = value
    form = ComparisonForm(post)
    assert form.is_valid(), form.errors
    return form.scenario()


def submit(client, post):
    return client.post(URL, post.urlencode(), content_type="application/x-www-form-urlencoded")


@pytest.mark.parametrize("case,index,credit_cbs,credit_ibs", [
    ("zero", 0, 0, 0), ("middle", 1, 1500, 15), ("high", 2, 3000, 30)])
def test_c01_c04_c05_reference(case, index, credit_cbs, credit_ibs):
    memory = compare(scenario(case))
    traditional, hybrid = memory["traditional"], memory["hybrid"]
    ref = REFERENCE["hypothetical_sensitivity"]
    assert traditional["das"]["exact"] == D(REFERENCE["monthly"]["monthly_das"])
    assert hybrid["effective_percent"] == D(REFERENCE["monthly"]["retained_rate"]) * 100
    assert abs(hybrid["regular"]["base"] - D(ref["sales_base"])) < D("1e-22")
    assert abs(hybrid["revenue"] - D(ref["revenue"])) < D("1e-22")
    assert abs(hybrid["das"]["exact"] - D(ref["retained_das"])) < D("1e-22")
    assert [hybrid["regular"][k].quantize(CENT) for k in ("cbs","ibs")] == [D("8837.42"), D("88.37")]
    assert hybrid["net"].quantize(CENT) == D(ref["cases"][index]["estimate"])
    assert hybrid["gross"].quantize(CENT) == D("15717.31")
    assert set(row["tax"] for row in hybrid["das"]["rows"]) == {"IRPJ", "CPP", "CSLL", "ICMS"}
    assert hybrid["accounts"]["cbs"]["used"] == credit_cbs
    assert hybrid["accounts"]["ibs"]["used"] == credit_ibs
    assert hybrid["accounts"]["cbs"]["acquisition"]["potential"] == 3000
    assert memory["difference"]["amount"].quantize(CENT) == D(ref["cases"][index]["estimate"]) - 8825
    assert memory["difference"]["traditional_burden"] == D("8.825")
    assert memory["guide"] is None and memory["engines"] == []
    assert all(len(s["states"]) == 5 for s in (memory, hybrid, traditional))


@pytest.mark.parametrize("changes", [{"cbs_rate": ""}, {"accept_cbs": ""}, {"exclusions": ""},
    {"exclusion_origin": "unknown"}])
def test_unknown_sale_preserves_other_components(changes):
    m = compare(scenario(**changes))
    assert m["traditional"]["das"]["displayed"] == 8825 and m["hybrid"]["regular"]["debit"] is None
    assert m["hybrid"]["effective_percent"] == D("7.457125")
    assert m["hybrid"]["accounts"]["cbs"]["available"] == 1500 and m["difference"] is None


def test_catalog_official_nominal_and_terms():
    rules = edition.regular_rules(MARCH)
    assert rules["cbs_applicable"] is None
    # Synthetic future catalog fixture exercises precedence, not an official rate for 2027.
    assert edition.cbs_rate(dict(rules, cbs_applicable="6.75"), D(10), True)[0] == D("6.75")
    assert edition.cbs_rate(rules, D(10), False)[0] is None
    with pytest.raises(edition.CatalogError):
        edition.regular_rules(date(2029, 1, 1))


def test_independent_histories_and_future_window():
    separate = compare(scenario(history_basis="estimated", hybrid_income="80000"))
    assert separate["traditional"]["history"]["total"] == 1200000
    assert separate["hybrid"]["history"]["total"] == 960000
    assert separate["hybrid"]["global_percent"] == D("8.35625")
    assert separate["hybrid"]["history"]["origin"] == "estimado"
    unknown = compare(scenario(history_basis="unknown"))
    assert not unknown["hybrid"].get("history") and unknown["difference"] is None
    assert unknown["hybrid"]["regular"]["ibs"] is not None
    outside = compare(scenario(history_basis="estimated", hybrid_income="60000"))
    assert outside["hybrid"]["band"]["number"] == 3 and outside["hybrid"]["das"] is None
    excess = compare(scenario(hybrid_prior_year="5000000"))
    assert excess["traditional"]["das"] and excess["difference"] is None
    changes = {"hybrid_" + m: "100000" for m in history_window(MARCH)}
    changes["hybrid_2026-02"] = "80000"
    real = compare(scenario(history_basis="real", **changes))
    assert real["hybrid"]["history"]["total"] == 1180000
    assert real["traditional"]["history"]["series"]["2026-02"] == 100000
    carried = dict(real["hybrid"]["history"]["series"], **{"2027-02": D(150000)})
    assert sum(carried[m] for m in history_window(APRIL)) == 1250000


def test_c05_c06_acquisition_and_events():
    assert compare(scenario(cbs_credit=""))["hybrid"]["accounts"]["cbs"]["net"] is None
    assert compare(scenario(credit_rule="unknown"))["hybrid"]["accounts"]["cbs"]["acquisition"]["assessed"] == 1500
    for changes in (dict(credit_evidence=""), dict(credit_origin="unknown"), dict(event_month=""),
                    dict(supplier="unknown"), dict(supplier="simples")):
        m = compare(scenario(**changes))
        assert m["difference"] is None and m["hybrid"]["gross"] is not None
    data = scenario(credit_rule="exception", event_month="2027-04")
    assert acquisition(data, "cbs", MARCH)["appropriated"] == 0
    assert acquisition(data, "cbs", APRIL)["appropriated"] == 1500
    data = scenario(supplier="simples", cbs_transfer="85.17", ibs_transfer="1.12", credit_rule="declared")
    assert acquisition(data, "cbs", MARCH)["appropriated"] == D("85.17")
    assert acquisition(data, "ibs", MARCH)["appropriated"] == D("1.12")
    exempt = scenario("zero", supplier="exempt", cbs_potential="", ibs_potential="")
    assert acquisition(exempt, "ibs", MARCH)["appropriated"] == 0
    partial = compare(scenario(ibs_credit=""))
    assert partial["hybrid"]["accounts"]["cbs"]["used"] == 1500
    assert partial["gross_difference"] and partial["difference"] is None


def test_c07_buyer_separate():
    consumer = compare(scenario())
    for buyer, expected in (("consumer", 0), ("simples", 0), ("unknown", None), ("regular", None)):
        m = compare(scenario(buyer=buyer))
        assert m["customer"]["traditional"]["cbs"]["usable"] == expected
        assert m["difference"] == consumer["difference"]
    m = compare(scenario(buyer="regular",buyer_document="on",buyer_traditional_cbs="28",buyer_hybrid_cbs="65"))
    assert m["customer"]["traditional"]["cbs"] == {"potential": D(28), "usable": None}
    assert m["customer"]["hybrid"]["cbs"]["potential"] == 65


@pytest.mark.parametrize("day,start", [("2026-08-31", None), ("2026-09-01", "2027-01-01"),
    ("2026-10-30","2027-01-01"), ("2026-10-31",None), ("2027-03-31","2027-07-01"),
    ("2027-04-01", None), ("2027-09-30","2028-01-01")])
def test_c14_window(day,start):
    begin, _ = window(date.fromisoformat(day), edition.regular_rules(MARCH))
    assert (begin.isoformat() if begin else None) == start


@pytest.mark.parametrize("changes,active", [(dict(option_status="absent", option_date=""), False),
    (dict(option_status="unknown",option_date=""), None), (dict(option_date="2026-11-01"), False),
    (dict(option_date="2027-03-01"), False), (dict(cancel_date="2026-12-20"), False),
    (dict(cancel_date="2026-12-21"), None), (dict(), None), (dict(option_status="active"), True)])
def test_c14_election(changes,active):
    m = compare(scenario(**changes))
    assert m["option"]["active"] is active and m["option"]["new_option_start"] == date(2027,7,1)
    assert "condicionais" in m["states"]["eligibility"]
    july = election(scenario(option_date="2027-03-31", option_status="active"), date(2027,7,1), edition.regular_rules(MARCH))
    assert july["active"] is True and july["first_term_end"] == date(2027,12,31)
    assert compare(scenario(option_status="active", refund="yes"))["option"]["return_start"] is None
    assert compare(scenario(option_status="active", refund="no"))["option"]["return_start"] == date(2027,7,1)
    assert compare(scenario(option_status="active", decision_date="2026-09-01"))["option"]["return_start"] is None


def test_c17_c18_accounts_are_independent():
    with localcontext(POLICY):
        empty = D(0)
        cbs = account(D(20),D(30),empty,empty,empty,empty,True)
        ibs = account(D(5),empty,empty,empty,empty,empty,True)
        assert (cbs["net"], cbs["closing"], ibs["net"]) == (0,10,5)
        april = account(D(12),empty,cbs["closing"],D(3),D(1),None,True)
        assert (april["available"],april["used"],april["closing"],april["remaining"]) == (12,12,0,None)
        settled = account(D(20),D(15),empty,empty,empty,D(4),True)
        assert (settled["net"],settled["remaining"]) == (5,1)
        over = account(D(20),D(15),empty,empty,empty,D(6),True)
        assert over["reconciliation_required"] and over["remaining"] is None
        assert account(D(5),empty,None,empty,empty,empty,True)["net"] is None
        assert account(D(5),empty,empty,empty,empty,empty,False)["net"] is None
        with pytest.raises(AccountError):
            account(D(5),D(1),empty,empty,D(2),empty,True)
    assert compare(scenario())["hybrid"]["regular"]["ibs_rounding_residue"] == CENT
    sn_item = REFERENCE["cases"][1]["body"]["total"]
    assert D(sn_item["totalTributos"])*1000 - (D("15.0025")+D("1352.8725")) == D("2.125")


def test_c19_different_prices_and_missing_basis():
    target = D("95675.75")
    h = target / (1 - D("0.02956375"))
    price = h + D("0.101") * (h - 2700)
    assert price.quantize(CENT) == D("108275.39")
    basis = dict(final_price=D(100000), period=MARCH, scope="obrigação")
    for mismatch in (dict(final_price=price), dict(period=APRIL), dict(scope="guia após extinções")):
        assert differences(D(8825), D("15717.31"), basis, dict(basis, **mismatch)) is None
    assert differences(D(8825), None, basis, basis) is None
    zero = compare(scenario("zero", revenue="0", exclusions="0"))
    assert zero["difference"]["amount"] == 0 and zero["difference"]["percent"] is None


@pytest.mark.parametrize("changes", [dict(period="2027-04", event_month="2027-04"), dict(activity="service"),
    dict(standing="impediment"), dict(opening="2027-01"), dict(profile="special")])
def test_excluded_profiles(changes):
    m = compare(scenario(**changes))
    assert m["difference"] is None and "accounts" not in m["hybrid"]


@pytest.mark.parametrize("changes", [dict(cbs_rate="1e-3"),dict(cbs_rate="100.01"),
    dict(revenue="1,001"),dict(exclusions="200000"),dict(edition="sn-03-02"),dict(ibs_state="1"),
    dict(zero_movements="on",ibs_opening="2"),dict(accept_cbs="bogus"),dict(event_month="2027-02")])
def test_reject_invalid_post(client, changes):
    post = example_post("zero")
    for key, value in changes.items():
        post[key] = value
    assert submit(client,post).status_code == 400


def test_security_and_replay(tmp_path):
    client = Client(enforce_csrf_checks=True)
    r = client.get(URL)
    post = example_post("high")
    assert submit(client,post).status_code == 403
    post["csrfmiddlewaretoken"] = r.cookies["csrftoken"].value
    r = submit(client,post)
    assert r.status_code == 200 and "no-store" in r["Cache-Control"]
    assert client.get(URL+"?price=1").status_code == 400
    assert client.post(URL,data="x"*65537,content_type="application/x-www-form-urlencoded").status_code == 413
    assert client.post(URL,data="{}",content_type="application/json").status_code == 415
    assert set(client.cookies) == {"csrftoken"}
    saved = json.loads(r.context["replay"])
    target = tmp_path / "sample.json"
    target.write_text(json.dumps(saved),encoding="utf-8")
    call_command("replay_comparison",target)
    saved["catalog_sha256"] = "tampered"
    target.write_text(json.dumps(saved),encoding="utf-8")
    with pytest.raises(CommandError, match="Divergência"):
        call_command("replay_comparison",target)
    post.appendlist("revenue","1")
    assert submit(client,post).status_code == 400


def test_c20_regular_catalog_fails_independently(monkeypatch, tmp_path):
    data = scenario()
    monkeypatch.setattr(edition, "ROOT", tmp_path)
    m = compare(data)
    assert m["traditional"]["das"]["displayed"] == 8825 and m["difference"] is None
    assert m["hybrid"]["effective_percent"] == D("7.457125")
    assert m["states"]["technical"] == "Parâmetros indisponíveis"


def test_volume_is_shared_without_document_extrapolation():
    m = compare(scenario(quantity="10000"))
    assert m["traditional"]["basis"]["quantity"] == m["hybrid"]["basis"]["quantity"] == 10000
    assert m["hybrid"]["net"].quantize(CENT) == D("14202.31") and m["engines"] == []


def test_example_rejects_duplicate_token():
    client = Client(enforce_csrf_checks=True)
    token = client.get(URL).cookies["csrftoken"].value
    response = client.post(URL, f"example=high&csrfmiddlewaretoken={token}&csrfmiddlewaretoken={token}",
                           content_type="application/x-www-form-urlencoded")
    assert response.status_code == 400 and response.context["memory"] is None


def test_error_summary_links_to_single_field_message(client):
    fields = example_post("middle")
    fields["cbs_rate"] = "101"
    response = submit(client, fields)
    html = response.content.decode()
    assert response.status_code == 400
    assert html.count('id="id_cbs_rate_error"') == 1
    assert 'aria-describedby="id_cbs_rate_error"' in html
    assert 'href="#id_cbs_rate"' in html


def test_subcent_obligation_distinguished_from_zero(client):
    fields = example_post("zero")
    fields["revenue"] = "0.01"
    fields["exclusions"] = "0"
    response = submit(client, fields)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Entre zero e R$ 0,01" in html and "R$ 0,00" in html
    assert "esse resíduo do híbrido é R$ 0,01" in html
    assert money(D("-0.001")) == "Entre −R$ 0,01 e zero"
    assert money(None) == "Em aberto"


def test_parallel_comparison_sessions():
    def run(case):
        client = Client(enforce_csrf_checks=True)
        token = client.get(URL).cookies["csrftoken"].value
        response = client.post(URL, f"example={case}&csrfmiddlewaretoken={token}",
                               content_type="application/x-www-form-urlencoded")
        assert response.status_code == 200
        replay = response.content.decode().split("<pre>", 1)[1].split("</pre>", 1)[0]
        memory = json.loads(unescape(replay))
        assert memory["inputs"]["example_origin"] == case
        assert set(client.cookies) == {"csrftoken"}
        return D(memory["hybrid"]["net"]).quantize(CENT)

    with ThreadPoolExecutor(max_workers=4) as workers:
        amounts = list(workers.map(run, ["zero", "middle", "high"] * 4))
    assert amounts == list(map(D, ["15717.31", "14202.31", "12687.31"])) * 4


def test_c20_simples_catalog_fails_independently(monkeypatch, tmp_path):
    from parameters import catalog
    data = scenario()
    monkeypatch.setattr(catalog, "ROOT", tmp_path)
    m = compare(data)
    assert m["hybrid"]["regular"]["cbs"].quantize(CENT) == D("8837.42")
    assert m["hybrid"]["accounts"]["ibs"]["used"] == 15
    assert m["difference"] is None and m["states"]["technical"] == "Parâmetros indisponíveis"
