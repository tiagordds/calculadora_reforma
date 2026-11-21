"""Coordinate a stateless simulation from normalized inputs, pinned to one edition."""
import hashlib
from datetime import date, datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path

from parameters.catalog import ACTIVE, ASSUMPTIONS_HASH, DIGESTS, CatalogError, resolve
from simulation.history import InputError, build_history
from tax.traditional import POLICY, assess, annual_excesses, band_for, history_window, shift_month

PERIOD = date(2027, 3, 1)
SOFTWARE = "simples-tradicional-04.1"
RULES = "SN-I-03.1"
ROOT = Path(__file__).resolve().parents[1]


def source_digest():
    digest = hashlib.sha256()
    for name in ("tax/traditional.py", "parameters/catalog.py", "simulation/history.py",
                 "simulation/traditional.py", "web/traditional_form.py"):
        digest.update(name.encode() + b"\0" + (ROOT / name).read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


SOFTWARE_HASH = source_digest()


def profile_issues(data):
    reasons = []
    if data["period"] != PERIOD:
        reasons.append("A competência habilitada é março de 2027.")
    if data["opening"] > shift_month(PERIOD, -13):
        reasons.append("A empresa precisa estar pelo menos no 14º mês de atividade.")
    if data["activity"] != "retail":
        reasons.append("Apenas revenda convencional de caneta é coberta. Serviços, inclusive os sujeitos ao Fator R, indústria e atividades mistas exigem outra apuração.")
    if data["place"] != "local":
        reasons.append("A loja e a entrega da venda interna devem estar em Florianópolis/SC.")
    if data["profile"] == "unknown":
        reasons.append("Confirme se as vendas da loja correspondem ao perfil descrito para estimar a guia.")
    elif data["profile"] != "ordinary":
        reasons.append("O cálculo exige uma loja com vendas homogêneas por NF-e 55, sem tratamentos especiais, receitas não segregadas, fatos externos ou resíduos do regime de caixa.")
    if data["standing"] == "impediment":
        reasons.append("Foi informado um impedimento vigente para o Simples Nacional nesta competência.")
    if data["standing"] == "regular":
        reasons.append("A opção regular de IBS e CBS informada exige outra apuração.")
    return reasons


def initial_memory(data, revision):
    return {
        "software": SOFTWARE, "software_sha256": SOFTWARE_HASH, "rules": RULES,
        "processed_at": datetime.now(timezone.utc).isoformat(), "engines": [],
        "engine_note": "Motores oficiais não utilizados nesta apuração.",
        "catalog_revision": revision, "catalog_sha256": DIGESTS.get(revision),
        "assumptions_sha256": ASSUMPTIONS_HASH,
        "inputs": data,
        "input_origins": {key: "não disponível" if value is None else "informado"
                          for key, value in data.items() if key not in ("edition", "history")},
        "edition_origin": "Revisão fixada pelo servidor.",
        "window": history_window(PERIOD) if data["period"] == PERIOD else None,
        "reasons": [], "conditions": [],
        "guide": None, "net_payable": None,
        "states": {"technical": "Sucesso", "completeness": "Não calculado", "nature": "Estimativa",
                   "validation": "Pendente de validação fiscal", "eligibility": "Elegibilidade não confirmada"},
    }


def screen_annual(data, history, parameters, memory):
    period = data["period"]
    known = {period.year: Decimal(0), period.year - 1: Decimal(0)}
    if history["revenue"] is not None:
        known[period.year] += history["revenue"]
    for month, value in history["series"].items():
        known[int(month[:4])] += value
    findings = []
    for year, key in ((period.year - 1, "prior_year"), (period.year, "year_to_date")):
        declared = data[key]
        if declared is not None and declared < known[year]:
            raise InputError(f"O acumulado de {year} é menor que as receitas já consideradas nesse ano. Confira o histórico e a receita de março.")
        if (declared is not None and year == period.year - 1 and data["opening"].year == year
                and data["opening"].month == 2 and history["origin"] == "informado" and declared != known[year]):
            raise InputError("Os meses reais desde a abertura cobrem todo o faturamento de 2026. Confira o total anual.")
        if declared is None:
            memory["conditions"].append(f"Receita acumulada de {year} não informada. Confirme limites e excessos.")
        amount = known[year] if declared is None else declared
        before = (declared - history["revenue"] if year == period.year and declared is not None
                  and history["revenue"] is not None else None)
        limits = parameters if year == period.year else parameters["prior_year_limits"]
        for finding in annual_excesses(amount, year, data["opening"], period, limits, before):
            finding["basis"] = "acumulado declarado" if declared is not None else "mínimo derivado das receitas consideradas"
            findings.append(finding)
    memory["excesses"] = findings
    for finding in findings:
        magnitude = "acima de 20%" if finding["above_twenty"] else "até 20%"
        memory["reasons"].append(f"Excesso em {finding['year']} ({magnitude}). Efeito previsto: "
                                 f"{finding['effect']} a partir de {finding['start']}.")
    if findings:
        memory["states"]["eligibility"] = "Fora da cobertura do sistema"
        for finding in findings:
            if finding["kind"] == "annual_limit" and finding["year"] < period.year and data["prior_year"] is not None:
                memory["states"]["eligibility"] = "Não elegível (limite excedido no ano anterior, conforme declaração)"
            if (finding["kind"] == "annual_limit" and finding["year"] == period.year
                    and data["year_to_date"] is not None and history["revenue_origin"] == "informado"
                    and data["year_to_date"] - history["revenue"] > finding["threshold"] * (
                        1 + Decimal(parameters["excess_margin"]) / 100)):
                memory["states"]["eligibility"] = "Não elegível (excesso superior a 20% anterior ao período, conforme declaração)"


def screen_band(history, params, memory):
    band = band_for(history["total"], params["bands"])
    memory["band"] = band
    if band is None or band["number"] != 4:
        memory["reasons"].append("O histórico precisa superar R$ 720.000,00 e ficar em até R$ 1.800.000,00 para a quarta faixa do Anexo I.")
        if not memory["states"]["eligibility"].startswith("Não elegível"):
            memory["states"]["eligibility"] = "Fora da cobertura do sistema"
    return band


def simulate(data, revision=ACTIVE):
    memory = initial_memory(data, revision)
    states = memory["states"]
    memory["reasons"] = profile_issues(data)
    if memory["reasons"]:
        if data["standing"] == "impediment":
            states["eligibility"] = "Não elegível (impedimento informado)"
        elif data["profile"] == "unknown" and len(memory["reasons"]) == 1:
            states["technical"] = "Entrada inválida"
        else:
            states["eligibility"] = "Fora da cobertura do sistema"
        return memory
    try:
        catalog, params, assumptions = resolve(revision, data["period"])
        memory.update(sources=catalog["sources"], validity=[params["start"], params["end"]],
                      assumptions_revision=assumptions["revision"])
        memory["scope"] = {key: catalog[key] for key in ("id", "regime", "activity", "annex", "territory", "origin")}
        memory["screening_parameters"] = {k: params[k] for k in (
            "annual_limit", "annual_sublimit", "excess_margin", "prior_year_limits")}
        with localcontext(POLICY):
            history = build_history(data, data["period"])
            memory["history"] = history
            memory["assumptions"] = [assumptions[key] for key in history["accepted"]]
            memory["conditions"].append("Confirmar opção tradicional, receita global, quadro societário, limites e ausência de impedimentos no período.")
            screen_annual(data, history, params, memory)
            band = screen_band(history, params, memory)
            if not memory["reasons"]:
                memory["amounts"] = assess(history["revenue"], history["total"], band)
                memory["projection"] = assumptions["annual_projection"]
                memory["formulas"] = [
                    "RBT12 = soma das doze receitas da janela.",
                    "Efetiva (%) = (RBT12 × nominal / 100 − dedução) × 100 / RBT12.",
                    "DAS bruto = receita fiscal da competência × efetiva / 100.",
                    "Parcela analítica = DAS antes de arredondar × repartição / 100.",
                    "Resíduo = soma das parcelas exibidas − DAS global exibido.",
                    "Projeção condicional = 12 × DAS mensal exibido.",
                ]
                memory["rounding"] = ("Decimal, 34 dígitos. Art. 45-A: primeiro dígito descartado ≥ 5 sobe um "
                                      "centavo; mínimo de R$ 0,01 para valor positivo. Aplicado na exibição do "
                                      "global e das parcelas; distribuição operacional depende do PGDAS.")
                states["completeness"] = "Completo para o DAS bruto do perfil"
                if history["origin"] == "informado" and history["revenue_origin"] == "informado":
                    states["nature"] = "Calculado com receitas declaradas"
    except InputError as exc:
        states["technical"] = "Entrada inválida"
        memory["reasons"].append(str(exc))
    except CatalogError as exc:
        states["technical"] = "Parâmetros indisponíveis"
        memory["reasons"].append(str(exc))
    return memory
