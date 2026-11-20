import json
from pathlib import Path
from urllib.parse import urlencode
from unittest.mock import Mock

from django.test import Client
import pytest

from adapters.manifest import EngineError
from simulation.service import simulate_pen
from web import views


URL = "/operacao/caneta/"


def post(client, data):
    return client.post(URL, urlencode(data, doseq=True), content_type="application/x-www-form-urlencoded",
                       CONTENT_TYPE="application/x-www-form-urlencoded")


def test_read_and_csrf_never_call_engine(monkeypatch):
    engine = Mock(side_effect=AssertionError)
    monkeypatch.setattr(views, "simulate_pen", engine)
    client = Client(enforce_csrf_checks=True)
    initial = client.get(URL)
    assert initial.status_code == 200 and b"checked" not in initial.content
    assert client.head(URL).content == b""
    invalid = post(client, {"confirm_cbs": "yes"})
    assert invalid.status_code == 403
    assert invalid["X-Robots-Tag"] == "noindex, nofollow"
    assert "no-store" in invalid["Cache-Control"]
    assert client.put(URL).status_code == 403
    assert not engine.called


@pytest.mark.parametrize("data", [{}, {"confirm_cbs": "no"}, {"confirm_cbs": ["yes", "yes"]},
                                  {"confirm_cbs": "yes", "url": "https://example.invalid"},
                                  {"confirm_cbs": "yes", "baseCalculo": "0.00"}])
def test_input_allowlist(client, monkeypatch, data):
    monkeypatch.setattr(views, "simulate_pen", Mock(side_effect=AssertionError))
    assert post(client, data).status_code == 400


def test_c16_historical_exclusion(client, monkeypatch):
    monkeypatch.setattr(views, "simulate_pen", Mock(side_effect=AssertionError))
    root = Path(__file__).resolve().parents[2] / "docs/evidencias/00a"
    records = [r for r in json.loads((root / "replay.json").read_bytes())
               if r["input_from"] == "simples.json#cases.nfse_820001"]
    assert len(records) == 2
    data = json.loads((root / "simples.json").read_bytes())["cases"]["nfse_820001"]["input"]
    for record in records:
        body = record["body"]
        if record["reported_version"]["versaoDb"] == "V0059":
            assert body["total"]["totalTributos"] == "0.00"
            assert body["objetos"][0]["tribCalc"]["tpRBSN"] == 9
        else:
            assert body["objetos"][0]["estadoItem"] == "NAO_IMPLEMENTADO" and "total" not in body
        response = post(client, {"confirm_cbs": "yes", "tpDoc": data["tpDoc"],
                                 "cClassTrib": data["itens"][0]["cClassTrib"]})
        assert response.status_code == 400
        assert response.context["outcome"].result is None


def test_limits_and_method(client):
    assert client.get(URL + "?base=100").status_code == 400
    assert client.post(URL, "a" * 65537, content_type="application/x-www-form-urlencoded").status_code == 413
    assert client.post(URL, {}, content_type="application/json").status_code == 415
    assert client.delete(URL).status_code == 405


def test_positive_csrf_escaping_and_trace(monkeypatch, c03):
    client = Client(enforce_csrf_checks=True)
    client.get(URL)
    raw = c03["body"]["objetos"][0]["tribCalc"]["IBSCBS"]["gIBSCBS"]["gCBS"]
    raw["memoriaCalculo"] = "<b>memória</b>"
    transport = Mock(return_value={"headers": {"x-warning-dados-simulados": "6"}, "body": c03["body"]})
    monkeypatch.setattr(views, "simulate_pen", lambda **kw: simulate_pen(transport=transport, **kw))
    result = post(client, {"confirm_cbs": "yes", "csrfmiddlewaretoken": client.cookies["csrftoken"].value})
    assert result.status_code == 200 and transport.call_count == 1
    html = result.content.decode()
    assert "R$ 10,10" in html and "&lt;b&gt;memória&lt;/b&gt;" in html and "<b>memória" not in html
    assert "private" in result["Cache-Control"]


@pytest.mark.parametrize("error,status", [("unavailable", 503), ("timeout", 503), ("version", 502),
                                          ("contract", 502), ("busy", 429), ("rejected", 422), ("missing", 503)])
def test_failure_dimensions(error, status):
    outcome = simulate_pen(confirmed=True, transport=Mock(side_effect=EngineError(error)))
    assert outcome.status == status and outcome.result is None
    assert outcome.completeness == "Não calculado"
    assert outcome.eligibility == "Elegibilidade não confirmada"
    assert outcome.validation == "Pendente de validação fiscal"


def test_service_requires_confirmation():
    assert simulate_pen(confirmed="yes", transport=Mock(side_effect=AssertionError)).status == 400
