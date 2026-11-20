"""Phase 03 acceptance. Oracle amounts come from the 00B capture and manual cases."""
import json
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import date
from decimal import Decimal as D
from pathlib import Path
from urllib.parse import urlencode

import pytest
from django.test import Client
from django.urls import reverse
from django.core.management import call_command, CommandError

from parameters.catalog import ACTIVE, CatalogError, resolve, select_period, unique_keys
from simulation.history import build_history
from simulation.traditional import PERIOD, simulate
from tax.traditional import das_cents, history_window

URL = "/simples/tradicional/"
REFERENCE = Path(__file__).resolve().parents[1] / "docs/evidencias/00b/reference.json"


def fields(**changes):
    return dict(dict(edition=ACTIVE, period="2027-03", opening="2023-01", activity="retail",
                     place="local", profile="ordinary", standing="unknown", unit="monthly",
                     income="100.000,00", revenue="100000", accept_history="yes", mode="estimated"), **changes)


def post(client, data):
    return client.post(URL, urlencode(data, doseq=True), content_type="application/x-www-form-urlencoded")


def result(client, **changes):
    return post(client, fields(**changes)).context["memory"]


def test_c01_c17_memory(client, monkeypatch):
    import socket
    def forbid(*args):
        pytest.fail("Unexpected outbound connection")
    monkeypatch.setattr(socket.socket, "connect", forbid)
    memory = result(client)
    oracle = json.loads(REFERENCE.read_bytes())["monthly"]
    amounts = memory["amounts"]
    assert memory["history"]["total"] == 1200000
    assert amounts["effective_percent"] == D(oracle["rate"]) * 100
    assert amounts["gross"] == D(oracle["monthly_das"])
    assert {r["tax"]: r["exact"] for r in amounts["rows"]} == {k: D(v) for k, v in oracle["allocation"].items()}
    assert [r["displayed"] for r in amounts["rows"]] == list(map(D, ["485.38","308.88","3706.50","2956.38","1352.87","15.00"]))
    assert [r["effective_percent"] for r in amounts["rows"]] == list(map(D, [".485375",".308875","3.7065","2.956375","1.3528725",".0150025"]))
    assert amounts["monthly"] == 8825 and amounts["annual"] == 105900
    assert amounts["sum_displayed"] == D("8825.01") and amounts["residue"] == D(".01")
    assert sum(r["exact"] for r in amounts["rows"] if r["tax"] in ("IBS", "CBS")) == D("1367.875")
    item = json.loads(REFERENCE.read_bytes())["cases"][1]["body"]["objetos"][0]["tribCalc"]
    assert (D(item["vIBSSN"]) + D(item["vCBSSN"])) * 1000 == 1370
    assert memory["engines"] == [] and memory["guide"] is memory["net_payable"] is None
    assert set(memory["states"]) == {"technical","completeness","nature","validation","eligibility"}
    assert memory["history"]["accepted"] == ["constant_history"]
    assert len(memory["catalog_sha256"]) == len(memory["software_sha256"]) == 64


@pytest.mark.parametrize("value,expected", [("0","0.00"),(".0001",".01"),(".004",".01"),(".005",".01"),
                                          ("1.00499","1.00"),("1.005","1.01"),("1.006","1.01")])
def test_c17_45a(value, expected):
    assert das_cents(D(value)) == D(expected)


@pytest.mark.parametrize("key,value,reason", [
    ("activity","service","Fator R"), ("activity","mixed","mistas"), ("activity","industry","indústria"),
    ("opening","2027-01","14º"), ("opening","2026-03","14º"), ("period","2027-04","competência"),
    ("place","other","Florianópolis"), ("profile","cash","caixa"), ("profile","mixed","segregadas"),
    ("profile","special","tratamentos especiais"), ("profile","unknown","perfil"),
    ("standing","impediment","impedimento"), ("standing","regular","IBS e CBS")])
def test_c08_c09_c11_c14_coverage(client,key,value,reason):
    m = result(client, **{key:value})
    assert "amounts" not in m and any(reason in s for s in m["reasons"])
    expected = "Fora da cobertura"
    if value == "impediment":
        expected = "Não elegível"
    elif value == "unknown":
        expected = "Elegibilidade não confirmada"
    assert m["states"]["eligibility"].startswith(expected)


def test_c12_shift_and_refine(client):
    months = history_window(PERIOD)
    assert months[0] == "2026-02" and months[-1] == "2027-01" and len(months) == 12
    actual = dict.fromkeys(months, "100000")
    actual["2026-02"] = "80000"
    estimated = result(client)
    refined = result(client, mode="real", **{"month_"+k:v for k,v in actual.items()})
    assert refined["history"]["total"] == 1180000
    assert refined["history"]["origin"] == "informado" and not refined["assumptions"]
    assert refined["amounts"]["monthly"] == D("8793.22")
    for key in ("opening", "place","activity","revenue","prior_year","year_to_date","edition"):
        assert refined["inputs"][key] == estimated["inputs"][key]
    april = date(2027,4,1)
    series = dict(refined["history"]["series"])
    del series["2026-02"]
    series["2027-02"] = D(150000)
    assert build_history(dict(refined["inputs"], history=series), april)["total"] == 1250000


def test_c14_absence_zero_and_years(client):
    m = result(client, revenue="0", opening="2026-02", prior_year="1100000")
    assert m["amounts"]["monthly"] == 0 and m["history"]["total"] == 1200000
    assert m["inputs"]["year_to_date"] is None
    assert m["states"]["eligibility"] == "Elegibilidade não confirmada"
    assert result(client, revenue="",accept_period="yes")["history"]["revenue_origin"] == "estimado"
    assert result(client, revenue="")["states"]["technical"] == "Entrada inválida"
    assert "amounts" not in result(client, accept_history="")
    assert "amounts" not in result(client, mode="real")
    assert "amounts" not in result(client, year_to_date="99999.99")
    assert "amounts" not in result(client, revenue="5000000",year_to_date="")
    actual = {"month_"+m:"100000" for m in history_window(PERIOD)}
    actual["month_2026-02"] = "0"
    assert result(client, mode="real", income="", **actual)["history"]["total"] == 1100000
    assert "amounts" not in result(client, mode="real", prior_year="1", **actual)
    assert "amounts" not in result(client, mode="real", **dict(actual, **{"month_2026-02":""}))


def test_annual_estimate_preserves_cents(client):
    m = result(client, unit="annual",income="1200000,01",revenue="",accept_period="yes")
    h = m["history"]
    assert h["total"] == D("1200000.01") and h["revenue"] == 100000
    assert h["series"]["2026-02"] == D("100000.01")
    assert h["accepted"] == ["constant_history","average_period"]


@pytest.mark.parametrize("amount,band,nominal,deduction", [
    ("720000",3,"9.50","13860"), ("720000.01",4,"10.70","22500"),
    ("1800000",4,"10.70","22500"), ("1800000.01",5,"14.30","87300")])
def test_c21(client, amount, band, nominal, deduction):
    m = result(client, income=amount,unit="annual")
    assert m["band"]["number"] == band and D(m["band"]["nominal"]) == D(nominal)
    assert D(m["band"]["deduction"]) == D(deduction)
    assert ("amounts" in m) == (band == 4)


@pytest.mark.parametrize("kind,threshold", [("annual_sublimit",3600000),("annual_limit",4800000)])
@pytest.mark.parametrize("offset,pct,high,effect", [
    ("-0.01",1,False,None), ("0",1,False,None), ("0.01",1,False,"janeiro de 2028"),
    ("0",D("1.2"),False,"janeiro de 2028"), ("0.01",D("1.2"),True,"04/2027")])
def test_c10(client,kind,threshold,offset,pct,high,effect):
    amount = D(threshold)*pct+D(offset)
    m = result(client, year_to_date=str(amount))
    targets = [f for f in m["excesses"] if f["kind"]==kind]
    if effect:
        assert len(targets)==1 and targets[0]["above_twenty"] == high
        assert targets[0]["start"] == effect and "amounts" not in m
    else:
        assert not targets
    if amount <= 3600000:
        assert "amounts" in m


def test_c10_prior_year_and_earlier_crossing(client):
    m = result(client, prior_year="3600000.01")
    assert m["excesses"][0]["start"] == "janeiro de 2027"
    m = result(client, opening="2026-02", prior_year="3960000.01")
    assert "retroativo" in m["excesses"][0]["start"]
    m = result(client, year_to_date="4500000", revenue="0")
    assert "primeiro mês" in m["excesses"][0]["start"]


def test_c13_archived_concurrent_requests(client):
    data = result(client)["inputs"]
    def replay(revision):
        m = simulate(dict(data, edition=revision), revision)
        boundary = simulate(dict(data, edition=revision, unit="annual", income=D("720000")), revision)
        return m["catalog_revision"], m["catalog_sha256"], m["amounts"]["monthly"], boundary["band"]
    editions = ["sn-03-01",ACTIVE]*12
    with ThreadPoolExecutor(max_workers=6) as workers:
        runs = list(workers.map(replay, editions))
    assert [r[0] for r in runs] == editions and len({r[1] for r in runs})==2
    assert all(r[2]==8825 for r in runs)
    assert all(r[3] is None for r in runs[::2])
    assert all(r[3]["number"] == 3 for r in runs[1::2])
    assert simulate(data,"missing")["states"]["technical"] == "Parâmetros indisponíveis"


def test_c13_vigency_and_conflicts():
    catalog, period, _ = resolve(ACTIVE, PERIOD)
    for outside in (date(2026,12,31),date(2029,1,1)):
        with pytest.raises(CatalogError, match="vigência"):
            resolve(ACTIVE,outside)
    segments = [dict(period,end="2027-12-31"),dict(period,start="2028-01-01")]
    split = dict(catalog, periods=segments)
    assert select_period(split,ACTIVE,date(2027,12,31)) is segments[0]
    assert select_period(split,ACTIVE,date(2028,1,1)) is segments[1]
    for start, error in (("2027-12-31","Sobreposição"),("2028-01-02","Lacuna")):
        with pytest.raises(CatalogError,match=error):
            select_period(dict(catalog,periods=[segments[0],dict(segments[1],start=start)]), ACTIVE,PERIOD)
    for key,value in (("units",{}),("bands",[]),("bands",period["bands"]*2)):
        with pytest.raises(CatalogError):
            select_period(dict(catalog,periods=[dict(period,**{key:value})]),ACTIVE,PERIOD)
    damaged=deepcopy(catalog)
    damaged["periods"][0]["bands"][1]["shares"]["CBS"]="15.34"
    with pytest.raises(CatalogError,match="Repartição"):
        select_period(damaged,ACTIVE,PERIOD)
    with pytest.raises(CatalogError,match="duplicada"):
        json.loads('{"a":1,"a":2}',object_pairs_hook=unique_keys)


@pytest.mark.parametrize("value",["NaN","Infinity","1e5","-1","1,001","1.23.45","9"*13,"<script>"])
def test_financial_input(client,value):
    response = post(client,fields(income=value))
    assert response.status_code==400 and not response.context["memory"]


def test_security_and_private_refinement():
    client = Client(enforce_csrf_checks=True)
    assert reverse("traditional")==URL
    response = client.get(URL)
    assert post(client,fields()).status_code==403
    params=fields(csrfmiddlewaretoken=response.cookies["csrftoken"].value)
    for changes in ({"nominal":"0"},{"edition":"sn-03-01"},{"mode":["real","estimated"]},
                    {"month_2026-02":["0","100"]},{"month_2027-02":"100"},{"accept_period":"true"}):
        assert post(client,dict(params,**changes)).status_code==400
    for r in (post(client,params),client.get(URL+"?income=1")):
        assert "no-store" in r["Cache-Control"] and "noindex" in r["X-Robots-Tag"]
    assert client.get(URL+"?income=1").status_code==400
    assert client.post(URL,data="x"*65537,content_type="application/x-www-form-urlencoded").status_code==413
    assert client.post(URL,data="{}",content_type="application/json").status_code==415
    assert set(client.cookies)=={"csrftoken"}


def test_missing_file_blocks_month(client,monkeypatch,tmp_path):
    from parameters import catalog
    monkeypatch.setattr(catalog,"ROOT",tmp_path)
    r=post(client,fields())
    assert r.status_code==503 and "amounts" not in r.context["memory"]


@pytest.mark.parametrize("revision", ["sn-03-01", ACTIVE])
def test_replay_copied_json(client, tmp_path, revision):
    data = result(client)["inputs"]
    memory = simulate(dict(data, edition=revision), revision)
    target = tmp_path / "synthetic.json"
    target.write_text(json.dumps(memory, default=str), encoding="utf-8")
    call_command("replay_traditional", target)
    memory["amounts"]["monthly"] = "9999.99"
    target.write_text(json.dumps(memory, default=str), encoding="utf-8")
    with pytest.raises(CommandError, match="Divergência"):
        call_command("replay_traditional", target)


def test_c10_eligibility_timing(client):
    assert result(client, prior_year="4800000.01")["states"]["eligibility"].startswith("Não elegível")
    assert result(client, year_to_date="6000000")["states"]["eligibility"].startswith("Não elegível")
    assert result(client, year_to_date="5760000.01")["states"]["eligibility"].startswith("Fora da cobertura")
    finding = result(client, opening="2026-01", prior_year="5760000.01")["excesses"][-1]
    assert "retroativo" in finding["start"]
