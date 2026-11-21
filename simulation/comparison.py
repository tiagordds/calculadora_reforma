"""Compare the same month's sales. No document is synthesized from monthly turnover."""
import hashlib
from datetime import datetime, timezone
from decimal import Decimal, localcontext

from parameters import comparison as edition
from parameters.catalog import ASSUMPTIONS_HASH, DIGESTS, CatalogError, number, resolve
from simulation.economics import differences
from simulation.history import InputError, build_series
from simulation.traditional import PERIOD, ROOT, profile_issues, screen_annual, screen_band
from tax.credits import AccountError, account, acquisition, customer
from tax.option import election
from tax.regular import das_portion, sales
from tax.traditional import CENT, POLICY, assess, rate_numerator

TAXES = ("cbs", "ibs")
MODULES = ("parameters/catalog.py", "parameters/comparison.py", "simulation/history.py",
           "simulation/traditional.py", "simulation/comparison.py", "simulation/economics.py", "tax/traditional.py",
           "tax/regular.py", "tax/credits.py", "tax/option.py", "web/traditional_form.py",
           "web/comparison_form.py", "web/comparison_view.py")
digest = hashlib.sha256()
for module in MODULES:
    digest.update(module.encode() + b"\0" + (ROOT / module).read_bytes().replace(b"\r\n", b"\n"))
SOFTWARE_HASH = digest.hexdigest()


def section():
    return dict(reasons=[], conditions=[], states=dict(technical="Sucesso", completeness="Não calculado",
                nature="Cenário hipotético", validation="Pendente de validação fiscal",
                eligibility="Elegibilidade não confirmada"))


def path_inputs(data, hybrid):
    if not hybrid or data["history_basis"] == "shared":
        return data
    return dict(data, income=data["hybrid_income"], unit="monthly", history=data["hybrid_history"],
                mode=data["history_basis"], accept_history=data["history_basis"] == "estimated")


def monthly_path(data, params, revenue, hybrid, assumptions, table_error):
    path = section()
    path.update(revenue=revenue, das=None, guide=None, extinguished=None)
    if table_error:
        path["states"]["technical"] = "Parâmetros indisponíveis"
        path["reasons"].append(table_error)
        return path
    if hybrid and data["history_basis"] == "unknown":
        path["reasons"].append("Escolha como obter o histórico fiscal inicial do híbrido.")
        return path
    try:
        series = build_series(path_inputs(data, hybrid), PERIOD)
        history = dict(series, revenue=revenue, revenue_origin="derivado" if hybrid else "informado")
        path["history"] = history
        path["conditions"].extend(assumptions[key] for key in series["accepted"])
        annual = (dict(data, prior_year=data["hybrid_prior_year"], year_to_date=data["hybrid_year_to_date"])
                  if hybrid else data)
        band = screen_band(history, params, path)
        screen_annual(annual, history, params, path)
        if path["reasons"]:
            return path
        # The effective rates depend on the window alone, even with the current base open.
        path["global_percent"] = rate_numerator(series["total"], band) * 100 / series["total"]
        retained = (100 - number(band["shares"]["CBS"]) - number(band["shares"]["IBS"])) if hybrid else 100
        path["effective_percent"] = path["global_percent"] * retained / 100
        if revenue is not None:
            path["das"] = das_portion(assess(revenue, series["total"], band), hybrid)
            path["states"]["completeness"] = "Completo para o DAS do perfil"
        else:
            path["reasons"].append("A receita fiscal depende da composição do preço e da CBS.")
    except InputError as exc:
        path["reasons"].append(str(exc))
        path["states"]["technical"] = "Entrada inválida"
    return path


def monthly_accounts(data, regular, path):
    accounts = {}
    for tax in TAXES:
        group = acquisition(data, tax, PERIOD)
        movements = [data[tax + "_" + key] for key in
                     ("opening", "adjustment", "reversal", "extinguished")]
        if data["zero_movements"]:
            movements = [Decimal(0)] * 4
        try:
            ledger = account(regular[tax], group["appropriated"], *movements, data["account_scope"])
        except AccountError as exc:
            path["states"]["technical"] = "Entrada inválida"
            path["reasons"].append(f"{tax.upper()} · {exc}")
            ledger = dict(debit=regular[tax], net=None)
        ledger["acquisition"] = group
        if ledger["net"] is None:
            path["reasons"].append(f"{tax.upper()} · " + (group["reason"] if group["appropriated"] is None else
                "Confira débito, movimentos por tributo e abrangência da conta para calcular a compensação."))
        accounts[tax] = ledger
    return accounts


def evaluate(data, memory):
    p = data["revenue"]
    common_issues = profile_issues(data)
    if common_issues:
        for item in (memory, memory["traditional"], memory["hybrid"]):
            item["reasons"].extend(common_issues)
            item["states"]["eligibility"] = ("Não elegível (impedimento informado)" if data["standing"] == "impediment"
                                             else "Fora da cobertura do sistema")
        return
    table_error, params, sn_assumptions = "", None, None
    memory["sources"] = {}
    try:
        catalog, params, sn_assumptions = resolve(edition.SIMPLES, PERIOD)
        memory["sources"].update(catalog["sources"])
    except CatalogError as exc:
        table_error = str(exc)
        memory["states"]["technical"] = "Parâmetros indisponíveis"
        memory["reasons"].append(table_error)
    traditional = monthly_path(data, params, p, False, sn_assumptions, table_error)
    memory["traditional"] = traditional
    try:
        rules = edition.regular_rules(PERIOD)
        assumptions = edition.premises()
    except CatalogError as exc:
        hybrid = monthly_path(data, params, None, True, sn_assumptions, table_error)
        hybrid["states"].update(technical="Parâmetros indisponíveis",
                                completeness="Parcial" if hybrid.get("history") else "Não calculado")
        hybrid["reasons"].append(str(exc))
        memory["hybrid"] = hybrid
        raise
    memory.update(profile=rules["profile"], validity=[rules["start"], rules["end"]],
                  consulted=rules["consulted"], convention=assumptions["convention"])
    memory["sources"].update(rules["sources"])
    notes = memory["conditions"]
    notes.append("As duas trajetórias são alternativas condicionais. Verifique o enquadramento, os limites e o recibo no Portal.")
    if data["history_basis"] == "shared":
        notes.append(assumptions["shared_history"])
    for accepted in ("zero_movements", "account_scope"):
        if data[accepted]:
            notes.append(assumptions["simple_account" if accepted == "account_scope" else accepted])
    option = election(data, PERIOD, rules)
    memory["option"] = option
    cbs, rate_origin = edition.cbs_rate(rules, data["cbs_rate"], data["accept_cbs"])
    exclusions = data["exclusions"] if data["exclusion_origin"] != "unknown" else None
    state, city = number(rules["ibs_state"]), number(rules["ibs_city"])
    regular = sales(p, exclusions, cbs, state, city)
    hybrid = monthly_path(data, params, regular["revenue"], True, sn_assumptions, table_error)
    memory["hybrid"] = hybrid
    if cbs is None:
        hybrid["reasons"].append(rate_origin)
    if exclusions is None:
        hybrid["reasons"].append("Informe o total das exclusões legais e sua origem, inclusive para assumir zero.")
    hybrid.update(regular=regular, cbs_percent=cbs, cbs_origin=rate_origin, state_percent=state,
                  city_percent=city, exclusions=exclusions, exclusion_origin=data["exclusion_origin"])
    if hybrid["states"]["eligibility"] == "Elegibilidade não confirmada":
        hybrid["states"]["eligibility"] = option["status"]
    if traditional["states"]["eligibility"] == "Elegibilidade não confirmada":
        if data["refund"] == "yes":
            traditional["states"]["eligibility"] = "Retorno ao regime único vedado por ressarcimento"
        elif option["active"]:
            traditional["states"]["eligibility"] = "Contrafactual. Opção regular declarada vigente para março"
    accounts = monthly_accounts(data, regular, hybrid)
    hybrid.update(accounts=accounts, gross=None, net=None)
    if hybrid["das"] is not None and regular["debit"] is not None:
        hybrid["gross"] = hybrid["das"]["exact"] + regular["debit"]
        hybrid["gross_display_residue"] = (hybrid["das"]["displayed"] +
            sum(regular[tax].quantize(CENT) for tax in TAXES) - hybrid["gross"].quantize(CENT))
        if all(asset["net"] is not None for asset in accounts.values()):
            hybrid["net"] = hybrid["das"]["exact"] + sum(asset["net"] for asset in accounts.values())
            hybrid["net_display_residue"] = (hybrid["das"]["displayed"] +
                sum(asset["net"].quantize(CENT) for asset in accounts.values()) - hybrid["net"].quantize(CENT))
    hybrid["states"]["completeness"] = ("Completo no perímetro do cenário" if hybrid["net"] is not None else
                                        "Parcial" if regular["debit"] is not None or hybrid.get("history") else "Não calculado")
    regular["states"] = dict(hybrid["states"], technical="Sucesso",
        completeness="Completo para os débitos da venda" if regular["debit"] is not None else "Não calculado")
    for ledger in accounts.values():
        ledger["states"] = dict(hybrid["states"],
            technical="Sucesso" if "available" in ledger else "Entrada inválida",
            completeness="Completo para a obrigação após créditos" if ledger["net"] is not None else "Parcial")
    for path in (hybrid, traditional):
        if path["das"]:
            path["das"]["states"] = dict(path["states"], technical="Sucesso", completeness="Completo para o DAS do perfil")
        if path.get("excesses"):
            path["membership"] = "Há excesso na triagem anual. Confira o limite, o tributo e a data de efeito na memória."
        elif data["standing"] == "member":
            path["membership"] = "Permanência no Simples declarada. Confirme limites, sócios e impedimentos."
        else:
            path["membership"] = "Permanência no Simples não confirmada."
    memory["customer"] = customer(data)
    t = traditional["das"]["exact"] if traditional["das"] else None
    for path in (traditional, hybrid):
        path["basis"] = dict(final_price=p, period=data["period"], quantity=data["quantity"], basket="mesmas vendas da loja",
                             scope="IRPJ, CSLL, CPP, ICMS, IBS e CBS antes das demais extinções")
    memory["gross_difference"] = differences(t, hybrid["gross"], traditional["basis"], hybrid["basis"])
    memory["difference"] = differences(t, hybrid["net"], traditional["basis"], hybrid["basis"])
    if memory["difference"]:
        memory["states"]["completeness"] = "Completo no perímetro do cenário"
        memory["display_residue"] = (traditional["das"]["displayed"] +
            memory["difference"]["amount"].quantize(CENT) - hybrid["net"].quantize(CENT))
    else:
        memory["states"]["completeness"] = "Parcial" if t is not None or regular["debit"] is not None else "Não calculado"
    if any(item["states"]["technical"] == "Entrada inválida" for item in (traditional, hybrid)):
        memory["states"]["technical"] = "Entrada inválida"
    memory["states"]["eligibility"] = "Alternativas condicionais. Disponibilidade de cada modalidade indicada separadamente."


def compare(data):
    memory = section()
    memory.update(software="comparador-04.1", software_sha256=SOFTWARE_HASH, revision=edition.REVISION,
                  catalog_sha256=edition.RULE_HASH, simples_revision=edition.SIMPLES,
                  simples_sha256=DIGESTS[edition.SIMPLES], premises_sha256=edition.PREMISE_HASH,
                  simples_premises_sha256=ASSUMPTIONS_HASH, processed_at=datetime.now(timezone.utc).isoformat(),
                  inputs=data, price=data["revenue"], engines=[], traditional=section(), hybrid=section(),
                  engine_note="Apuração empresarial agregada em Python. Sem operações individuais informadas.",
                  difference=None, gross_difference=None, guide=None,
                  input_origins={key: ("ausente" if value is None or value == "" else "declarado no formulário")
                                 for key, value in data.items()},
                  formulas=["B = (P − X) / (1 + c + i), taxas em fração", "D = B × (c + i)", "H = P − D",
                            "DAS híbrido = H × efetiva × (1 − repartição CBS − repartição IBS)",
                            "Disponível = saldo inicial + apropriado + ajustes credores − estornos",
                            "Uso = mínimo entre disponível e débito ainda compensável do mesmo tributo",
                            "Líquido = débito − uso. Saldo final = disponível − uso",
                            "Diferença = híbrido − tradicional. Variação = diferença / tradicional",
                            "Carga sobre vendas = obrigação no perímetro / preço final comum"],
                  rounding="Decimal de 34 dígitos, HALF_UP. DAS exibido conforme art. 45-A. Somar antes de arredondar; a guia depende de conciliação.")
    memory["input_origins"].update(edition="edição fixada no servidor", period="competência verificada no servidor",
        history="meses fiscais informados ou média expressamente aceita", hybrid_history=data["history_basis"],
        exclusions=data["exclusion_origin"], cbs_rate="taxa de cenário sujeita a aceite",
        cbs_credit=data["credit_origin"], ibs_credit=data["credit_origin"])
    try:
        with localcontext(POLICY):
            evaluate(data, memory)
    except CatalogError as exc:
        memory["states"].update(technical="Parâmetros indisponíveis",
                                completeness="Parcial" if memory["traditional"].get("das") else "Não calculado")
        memory["reasons"].append(str(exc))
    return memory
