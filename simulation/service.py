from dataclasses import dataclass
from datetime import datetime, timezone
import json

from adapters.manifest import CALC_PATH, COMMIT, DB_HASH, EngineError, JAR_HASH
from adapters.regular import call
from adapters.result import OperationResult, interpret
from .example import pen_operation


@dataclass(frozen=True)
class Outcome:
    technical: str
    completeness: str = "Não calculado"
    nature: str = "Cenário hipotético"
    validation: str = "Pendente de validação fiscal"
    eligibility: str = "Elegibilidade não confirmada"
    error: str = ""
    status: int = 200
    result: OperationResult | None = None
    trace: str = ""
    replay: dict | None = None


def simulate_pen(*, confirmed, deadline=None, transport=call):
    if confirmed is not True:
        return Outcome("Entrada inválida", error="Confirme a hipótese de CBS para calcular.", status=400)
    payload = pen_operation()
    try:
        reply = transport(payload, deadline=deadline)
        result = interpret(payload, reply)
    except EngineError as exc:
        if exc.code in ("version", "contract"):
            return Outcome("Falha técnica", error=str(exc), status=502)
        if exc.code == "rejected":
            return Outcome("Entrada inválida", error=str(exc), status=422)
        return Outcome("Indisponibilidade", error=str(exc), status=429 if exc.code == "busy" else 503)
    trace = {
        "format_version": 1, "executed_at": datetime.now(timezone.utc).isoformat(),
        "scope": "C03 / 2027-03", "source": "docs/evidencias/00b/reference.json#cases[0]",
        "input_origin": "Exemplo sintético da revenda interna de caneta esferográfica comum",
        "ibs_source": "LC 214/2025 art. 344, transição de 2027; docs/TAX_SOURCES.md",
        "layout": "JSON de observabilidade do regular na revisão indicada",
        "hypothesis": "CBS de 10% aceita explicitamente no formulário",
        "rates_unit": "pontos percentuais", "currency": "BRL",
        "commit": COMMIT, "jar_sha256": JAR_HASH, "db_sha256": DB_HASH,
        "rounding": "Motor regular: intermediários a oito casas, HALF_EVEN, moeda a duas casas",
        "aggregation": "Soma decimal dos totais de CBS e IBS devolvidos pelo motor",
        "method": "POST", "path": CALC_PATH, "input": payload, **reply,
    }
    # Error catalog links may contain a private host. Only present code/title/pointer in that case.
    trace_text = json.dumps(trace, indent=2, ensure_ascii=False) if result.totals else ""
    return Outcome("Sucesso", result.completeness, result=result, trace=trace_text, replay=trace)
