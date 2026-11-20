from copy import deepcopy
from decimal import Decimal
import json

import pytest

from adapters.manifest import EngineError
from adapters.result import interpret
from simulation.example import pen_operation
from simulation.service import simulate_pen


def observed(body):
    return {"headers": {"x-warning-dados-simulados": "6"}, "body": body}


def test_c03_exact_wire_and_amounts(c03):
    assert json.dumps(pen_operation(), sort_keys=True) == json.dumps(c03["input"], sort_keys=True)
    result = interpret(pen_operation(), observed(c03["body"]))
    assert result.completeness == "Completo no recorte"
    assert result.totals.combined == Decimal("10.10")
    assert (result.totals.state_ibs, result.totals.city_ibs) == (Decimal(".05"), Decimal(".05"))
    assert result.items[0].amounts.cbs.as_tuple() == Decimal("10.00").as_tuple()
    assert len(result.items[0].memory) == 3


def test_mixed_preserves_zero_absence_and_subtotal(regular_cases):
    case = regular_cases["mixed_2027"]
    result = interpret(case["input"], observed(case["body"]))
    assert result.completeness == "Parcial"
    assert result.items[0].amounts.cbs == Decimal("0.00")
    assert result.items[-1].amounts is None
    assert result.items[-1].errors[0]["pointer"] == "#/itens/3/ncm"
    assert result.totals.cbs == Decimal("56.76")


def test_no_total_for_rejected_item(regular_cases):
    case = regular_cases["missing_rates_2027"]
    result = interpret(case["input"], observed(case["body"]))
    assert result.totals is None and result.completeness == "Não calculado"
    assert result.items[0].errors[0]["code"] == "REG-037"


@pytest.mark.parametrize("change", [
    "missing", "extra", "duplicate", "wrong_number", "bool_number", "unknown_state", "class",
    "base", "rate", "warning", "missing_memory", "missing_cbs", "errors_with_tax", "bad_total",
    "numeric_money", "zero_for_absent", "unbounded_money", "invalid_structure",
])
def test_c20_incoherent_reply(c03, change):
    reply = observed(deepcopy(c03["body"]))
    rows = reply["body"]["objetos"]
    row = rows[0]
    tax = row["tribCalc"]["IBSCBS"]
    group = tax["gIBSCBS"]
    changes = {
        "missing": rows.clear,
        "extra": lambda: rows.append(dict(row, nObj=2)),
        "duplicate": lambda: rows.append(row),
        "wrong_number": lambda: row.update(nObj=3),
        "bool_number": lambda: row.update(nObj=True),
        "unknown_state": lambda: row.update(estadoItem="CALCULADO"),
        "class": lambda: tax.update(cClassTrib="820001"),
        "base": lambda: group.update(vBC="99.99"),
        "rate": lambda: group["gCBS"].update(pCBS="9.8"),
        "warning": reply["headers"].clear,
        "missing_memory": lambda: group["gIBSMun"].pop("memoriaCalculo"),
        "missing_cbs": lambda: group["gCBS"].pop("vCBS"),
        "errors_with_tax": lambda: row.update(erros=[]),
        "bad_total": lambda: reply["body"]["total"]["tribCalc"]["IBSCBSTot"]["gCBS"].update(vCBS="0.00"),
        "numeric_money": lambda: group["gCBS"].update(vCBS=10),
        "zero_for_absent": lambda: group["gCBS"].update(vCBS=None),
        "unbounded_money": lambda: group["gCBS"].update(vCBS="1e1000"),
        "invalid_structure": lambda: reply["body"].update(objetos=None),
    }
    changes[change]()
    with pytest.raises(EngineError, match="contrato"):
        interpret(pen_operation(), reply)


def test_ambiguous_ids_same_count(regular_cases):
    case = regular_cases["mixed_2027"]
    case["body"]["objetos"][1]["nObj"] = 1
    with pytest.raises(EngineError):
        interpret(case["input"], observed(case["body"]))


def test_trace_preserves_original(c03):
    reply = {**observed(c03["body"]), "http": 200, "version": c03["version"]}
    outcome = simulate_pen(confirmed=True, transport=lambda *args, **kwargs: reply)
    trace = json.loads(outcome.trace)
    for key in ("input", "body", "commit", "jar_sha256", "db_sha256", "http", "version"):
        assert trace[key] == c03[key]
