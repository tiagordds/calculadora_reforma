"""C09. Assess two segregated revenues against one company's history."""
import hashlib
from decimal import Decimal, localcontext
from pathlib import Path

from parameters import retail, services
from parameters.catalog import DIGESTS, CatalogError
from simulation.services import example_inputs as service_example, known_excess
from tax.services import PAYROLL, factor_r, service_das, summarize_history
from tax.traditional import POLICY, assess, band_for, das_cents, history_window, shift_month

PERIOD = services.PERIOD
EDITION = f"{retail.REVISION}+{services.REVISION}"
GROUPS = ("retail", "service")
LABELS = {"retail": "Comércio", "service": "Serviços"}


def software_digest():
    digest = hashlib.sha256()
    root = Path(__file__).resolve().parents[1]
    for path in ("parameters/catalog.py", "parameters/retail.py", "parameters/services.py",
                 "tax/traditional.py", "tax/services.py", "simulation/services.py", "simulation/mixed.py",
                 "web/traditional_form.py", "web/services.py", "web/mixed.py"):
        digest.update(path.encode() + b"\0" + (root / path).read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


SOFTWARE_HASH = software_digest()


def example_inputs():
    data = service_example()
    del data["revenue"], data["treatment"]
    data.update(edition=EDITION, activity="mixed", retail="60000", service="40000",
                retail_treatment="ordinary", service_treatment="ordinary")
    for row in data["history"].values():
        del row["turnover"]
        row.update(retail="60000", service="40000", origin="synthetic")
    return data


def segregated_total(row):
    if any(row[key] is None for key in GROUPS):
        return None
    return sum(row[key] for key in GROUPS)


def enterprise_history(data):
    series = {}
    for month in history_window(PERIOD):
        row = data[month]
        missing = [key for key in (*GROUPS, *PAYROLL) if row[key] is None]
        series[month] = dict(row, turnover=segregated_total(row), missing=missing)
    return dict(summarize_history(series, PERIOD), series=series)


def exceeds_limit(data, history, sublimit):
    # Only this lower-bound check can use the known part of an incomplete month.
    def known(row):
        return sum(row[key] for key in GROUPS if row[key] is not None)

    lower_bounds = {month: {"turnover": known(row)} for month, row in history["series"].items()}
    return known_excess(dict(opening=data["opening"], history=lower_bounds, revenue=known(data)),
                        Decimal(sublimit))


def assess_group(group, data, annex, bands, basis, allowed, service_rules=None):
    revenue = data[group]
    band = band_for(basis, bands) if basis is not None and annex and bands else None
    reasons = []
    if data[group + "_treatment"] != "ordinary":
        reasons.append(f"{LABELS[group]} com condições especiais ou pendentes de confirmação.")
    if revenue is None:
        reasons.append(f"Informe a receita de março de {LABELS[group].lower()}.")
    if basis is not None and annex and bands and (band is None or "shares" not in band):
        reasons.append(f"{LABELS[group]} fora das cinco faixas qualificadas. Verifique sublimite e recolhimento externo.")
    result = dict(label=LABELS[group], revenue=revenue, annex=annex, band=band, reasons=reasons)
    if allowed and band and "shares" in band and not reasons:
        if group == "retail":
            amounts = assess(revenue, basis, band)
            del amounts["annual"]
        else:
            amounts = service_das(revenue, basis, band, service_rules)
        result["amounts"] = amounts
    return result


def consolidate(groups):
    with localcontext(POLICY):
        allocations = {}
        gross = sum(group["amounts"]["gross"] for group in groups)
        monthly = das_cents(gross)
        for group in groups:
            for row in group["amounts"]["rows"]:
                tax = row["tax"]
                allocations[tax] = allocations.get(tax, Decimal(0)) + row["exact"]
        rows = [dict(tax=tax, exact=value, displayed=das_cents(value)) for tax, value in allocations.items()]
        displayed = sum(row["displayed"] for row in rows)
        return dict(gross=gross, monthly=monthly, rows=rows, sum_displayed=displayed,
                    residue=displayed - monthly,
                    activity_residue=sum(group["amounts"]["monthly"] for group in groups) - monthly)


def simulate_mixed(data):
    history = enterprise_history(data["history"])
    memory = dict(inputs=data, software="mixed-01.1", software_sha256=SOFTWARE_HASH, editions={
        retail.REVISION: retail.DIGEST, retail.BASE: DIGESTS[retail.BASE], services.REVISION: services.DIGEST},
        engines=[], state="Parcial", reasons=[], history=history, revenue=segregated_total(data),
        scope="Março/2027, Florianópolis/SC. Revenda local de canetas nacionais e software sob encomenda "
              "no estabelecimento. Clientes privados, mercado interno e regime de competência.",
        eligibility="Opção e condições declaradas, sujeitas à conferência profissional.",
        method="Faixa pela RBT12 empresarial. Alíquota efetiva = (RBT12 × nominal − dedução) / RBT12, "
               "com nominal em fração e base substituta no caso de RBT12 zero. Aplicar cada efetiva "
               "à receita da atividade. Consolidar os valores analíticos por tributo.",
        guide=None, sources={}, validation="Estimativa interna. Homologação fiscal pendente.",
        rounding="34 dígitos nas divisões. Somar antes de arredondar ao centavo, metade para cima e mínimo positivo de R$ 0,01.")
    reasons = memory["reasons"]
    if data["period"] != PERIOD:
        reasons.append("A competência habilitada é março de 2027.")
    if data["opening"] > shift_month(PERIOD, -13):
        reasons.append("A empresa precisa estar ao menos no 14º mês de atividade.")
    if data["activity"] != "mixed":
        reasons.append("Confirme a revenda de canetas e o software sob encomenda em Florianópolis, sem outras atividades.")
    if data["regime"] != "traditional":
        reasons.append("Confirme a opção pelo Simples tradicional sem impedimento no período.")
    if reasons:
        memory["state"] = "Perfil fora da cobertura ou pendente de confirmação"
        return memory

    retail_rules = service_rules = None
    try:
        retail_rules = retail.load_retail(PERIOD)
        memory["sources"]["retail"] = retail_rules["source"]
    except CatalogError as exc:
        reasons.append(f"Parâmetros comerciais indisponíveis. {exc}")
    try:
        service_rules = services.load_rules()
        memory["sources"]["service"] = dict(references=service_rules["sources"], consulted=service_rules["consulted"],
                                            validity=[service_rules["start"], service_rules["end"]])
    except CatalogError as exc:
        reasons.append(f"Parâmetros de serviços indisponíveis. {exc}")
    memory["parameters_unavailable"] = retail_rules is None or service_rules is None
    known_rules = retail_rules or service_rules
    within = data["limits"] == "within" and known_rules is not None
    if known_rules and (not within or exceeds_limit(data, history, known_rules["annual_sublimit"])):
        within = False
        reasons.append("Excesso ou limite anual sem confirmação. Confira limite, sublimite e proporcionalidade na abertura.")

    turnover, payroll = history["rbt12r"], history["fs12"]
    if turnover is None:
        reasons.append("Complete as receitas históricas das duas atividades para determinar a faixa e o Fator R.")
    if payroll is None:
        reasons.append("Complete a folha empresarial para enquadrar o serviço.")
    factor = None
    if turnover is not None and payroll is not None and service_rules:
        factor = factor_r(payroll, turnover, service_rules)
    basis = turnover
    if turnover == 0:
        basis = Decimal(service_rules["zero_rate_basis"]) if service_rules else None
    memory.update(factor=factor, rate_basis=basis)
    annex = factor["annex"] if factor else None
    groups = [
        assess_group("retail", data, "I", retail_rules["bands"] if retail_rules else [], basis, within),
        assess_group("service", data, annex, service_rules["annexes"][annex] if annex else [], basis, within, service_rules),
    ]
    memory["groups"] = groups
    if all("amounts" in group for group in groups):
        memory["amounts"] = consolidate(groups)
        memory["state"] = "Estimativa condicionada às premissas informadas"
    return memory
