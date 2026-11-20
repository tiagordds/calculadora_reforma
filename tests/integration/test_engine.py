from datetime import datetime, timezone
import json

import pytest
import requests

from adapters.manifest import APP, CALC_PATH, COMMIT, DATABASE, DB_HASH, JAR_HASH, ORIGIN, READY, RUNTIME, VERSION_PATH
from adapters.regular import call
from adapters.result import interpret
from simulation.example import pen_operation


pytestmark = pytest.mark.engine_integration


def record(request, name, payload, reply):
    directory = request.config.getoption("--record-engine")
    if directory:
        directory.mkdir(exist_ok=True, parents=True)
        data = {
            "executed_at": datetime.now(timezone.utc).isoformat(), "case": name,
            "commit": COMMIT, "jar_sha256": JAR_HASH, "db_sha256": DB_HASH,
            "method": "POST", "path": CALC_PATH, "input": payload, **reply,
        }
        (directory / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")


@pytest.mark.parametrize("document", [None, 55], ids=["original", "nf-e-55"])
def test_c03_real(c03, document, request):
    payload = pen_operation()
    assert payload == c03["input"]
    if document is not None:
        payload["tpDoc"] = document
    reply = call(payload)
    assert reply["http"] == 200
    assert reply["version"] == c03["version"]
    assert reply["headers"] == {"x-calc-app-version": APP, "x-calc-db-version": DATABASE,
                                "x-warning-dados-simulados": "6"}
    assert reply["body"] == c03["body"]
    result = interpret(payload, reply)
    assert str(result.totals.combined) == "10.10"
    record(request, "c03" if document is None else "c03-tpdoc55", payload, reply)


def test_c15_real(regular_cases, request):
    case = regular_cases["mixed_2027"]
    reply = call(case["input"])
    result = interpret(case["input"], reply)
    assert result.completeness == "Parcial"
    assert reply["body"]["total"] == case["body"]["total"]
    assert [item.state for item in result.items] == [row["estadoItem"] for row in case["body"]["objetos"]]
    assert result.items[-1].errors[0]["code"] == "REG-011"
    record(request, "c15", case["input"], reply)


def test_backend_client_certificate_required():
    identity = RUNTIME / READY.read_text(encoding="ascii")
    with requests.Session() as anonymous:
        anonymous.trust_env = False
        with pytest.raises(requests.exceptions.SSLError):
            anonymous.get(ORIGIN + VERSION_PATH, verify=str(identity / "ca.pem"), timeout=2)
