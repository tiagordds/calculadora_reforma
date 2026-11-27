"""Monthly C08 alternatives at a common final price and service volume."""
import hashlib
from decimal import Decimal, localcontext
from pathlib import Path

from parameters import comparison as regular_edition
from parameters import services as service_edition
from parameters.catalog import CatalogError
from simulation.comparison import SOFTWARE_HASH as RETAIL_HASH, monthly_accounts, section
from simulation.economics import differences
from simulation.services import SOFTWARE_HASH as SERVICE_HASH, simulate_services
from tax.option import election
from tax.regular import das_portion, sales
from tax.service_regular import service_turnover
from tax.traditional import POLICY

PERIOD = service_edition.PERIOD
REVISION = "services-hybrid-01"
ROOT = Path(__file__).resolve().parents[1]
digest = hashlib.sha256((SERVICE_HASH + RETAIL_HASH).encode())
for filename in ("simulation/service_comparison.py", "web/service_comparison.py", "tax/service_regular.py"):
    digest.update(filename.encode() + b"\0" + (ROOT / filename).read_bytes().replace(b"\r\n", b"\n"))
SOFTWARE_HASH = digest.hexdigest()


def path_assessment(data, history, revenue, hybrid, basis):
    # The gross equivalent is the common starting point for art. 22-A in either path.
    inputs = {k: data[k] for k in ("period", "opening", "activity", "treatment", "limits", "origin", "regime")}
    if inputs["regime"] == "member":
        inputs["regime"] = "traditional"  # Calculate the unified gross equivalent before selecting the retained taxes.
    # With turnover open, this probe obtains only historical rates. Suppress its amounts
    # and repeat the annual screening on the actual fiscal turnover before using them.
    inputs.update(history=history, revenue=revenue if revenue is not None else Decimal(0))
    assessment = simulate_services(inputs)
    path = section()
    path.update({k: assessment[k] for k in ("factor", "band", "rate_basis", "history", "sources", "rounding")
                 if k in assessment})
    path.update(revenue=revenue, reasons=assessment["reasons"], das=None, iss_percent=None, basis=dict(basis),
                history_origin=data["history_basis"] if hybrid else data["origin"])
    if assessment["state"] == "Parâmetros indisponíveis":
        path["states"]["technical"] = assessment["state"]
    if "amounts" in assessment:
        rows = assessment["amounts"]["rows"]
        path["iss_percent"] = next(row["effective_percent"] for row in rows if row["tax"] == "ISS")
    if revenue is None:
        path["reasons"].append("A receita fiscal híbrida de março está em aberto.")
    elif "amounts" in assessment:
        path["das"] = das_portion(assessment["amounts"], hybrid)
        path["das"]["iss_capped"] = assessment["amounts"]["iss_capped"]
        path["states"]["completeness"] = "Completo para o DAS do perfil"
    elif "history" in path:
        path["states"]["completeness"] = "Parcial"
    return path


def service_sales(data, hybrid, rules, eligible, notes):
    price = data["revenue"]
    cbs, origin = regular_edition.cbs_rate(rules, data["cbs_rate"], data["accept_cbs"])
    state, city = (Decimal(rules[k]) for k in ("ibs_state", "ibs_city"))
    extra = data["exclusions"] if data["exclusion_origin"] != "unknown" else None
    iss = data["iss_amount"] if data["iss_basis"] == "document" else None
    share = None
    if data["iss_basis"] == "proportional" and hybrid["iss_percent"] is not None:
        share = hybrid["iss_percent"] / 100
    if eligible:
        result = service_turnover(price, data["hybrid_revenue"], iss, share, extra, cbs, state, city)
        if result["issue"]:
            notes.append(result["issue"])
    else:
        result = dict(sales(price, None, cbs, state, city), iss_excluded=None)
    result["revenue_origin"] = "informada" if eligible and data["hybrid_revenue"] is not None else "derivada do preço"
    if cbs is None:
        notes.append(origin)
    if eligible and result["iss_excluded"] is None:
        notes.append("Falta o ISS excluível identificado ou a hipótese proporcional com anexo e base suficientes.")
    if extra is None:
        notes.append("Informe as demais exclusões do preço e sua origem, inclusive para assumir zero.")
    result.update(other_exclusions=extra, iss_share=share,
                  cbs_percent=cbs, cbs_origin=origin, state_percent=state, city_percent=city)
    return result


def compare_services(data):
    basis = dict(period=data["period"], final_price=data["revenue"], quantity=data["quantity"],
                 basket="mesmas prestações privadas de software sob encomenda",
                 scope="IRPJ, CSLL, CPP, ISS, IBS e CBS antes das demais extinções")
    memory = section()
    memory.update(revision=REVISION, software_sha256=SOFTWARE_HASH, inputs=data, engines=[], difference=None,
                  catalogs={service_edition.REVISION: service_edition.DIGEST,
                            regular_edition.REVISION: regular_edition.RULE_HASH},
                  document="NFS-e sem combinação qualificada. Item 1.04, atividade 09 e NBS 1.1502.20.00 candidatos. C16 excluído.",
                  guide=None, payment=None, customer=dict(cbs=None, ibs=None,
                      reason="Crédito potencial do cliente depende do seu regime e do DF-e idôneo de cada prestação. "
                             "No tradicional, limita-se ao IBS e à CBS efetivamente devidos na operação. "
                             "A apropriação exige conferir os arts. 47 e 48 da LC 214."))
    with localcontext(POLICY):
        traditional = path_assessment(data, data["history"], data["revenue"], False, basis)
        shared = data["history_basis"] == "shared"
        history = data["history"] if shared else data["hybrid_history"]
        hybrid = path_assessment(data, history, data["hybrid_revenue"], True, basis)
        memory.update(traditional=traditional, hybrid=hybrid)
        if data["origin"] == "synthetic":
            memory["conditions"].append("Exemplo sintético. Histórico, opção e créditos declarados pertencem ao ensaio.")
        if data["iss_basis"] == "proportional":
            memory["conditions"].append("Hipótese aceita de serviços homogêneos com ISS excluível igual à parcela efetiva do híbrido.")
        if shared:
            memory["conditions"].append("Igualdade aceita para os doze meses de receita e para cada componente de folha.")
        if data["destination"] == "public":
            for path in (traditional, hybrid):
                path.update(revenue=None, das=None, reasons=["O cliente público exige segregação fora do perfil C08."])
                path["states"]["completeness"] = "Fora do recorte"
            memory["reasons"].extend(traditional["reasons"])
            return memory
        if "history" not in traditional and traditional["states"]["technical"] == "Sucesso":
            memory["reasons"].extend(traditional["reasons"])
            return memory
        try:
            rules = regular_edition.regular_rules(data["period"])
            option = election(data, PERIOD, rules)
            memory.update(option=option, sources=rules["sources"], consulted=rules["consulted"])
            notes = []
            eligible = data["destination"] == "local" and data["treatment"] == "ordinary"
            if not eligible:
                notes.append("Confirme incidência ordinária e domicílio aplicável do adquirente privado em Florianópolis.")
            if option["active"] is False:
                notes.append(option["status"])
            regular = service_sales(data, hybrid, rules, eligible and option["active"] is not False, notes)
        except CatalogError as exc:
            memory["reasons"].append(str(exc))
            memory["states"].update(technical="Parâmetros indisponíveis", completeness="Parcial")
            return memory
        if hybrid["revenue"] != regular["revenue"]:
            hybrid = path_assessment(data, history, regular["revenue"], True, basis)
            memory["hybrid"] = hybrid
            if regular["iss_share"] is not None and hybrid["iss_percent"] is None and regular["base"] is not None:
                notes.append("A triagem anual impede estimar o ISS pela partilha. Identifique o valor excluível nos documentos.")
                regular.update(sales(data["revenue"], None, None, None, None), iss_excluded=None)
                regular["revenue"] = data["hybrid_revenue"]
                hybrid = path_assessment(data, history, regular["revenue"], True, basis)
                memory["hybrid"] = hybrid
        hybrid["states"]["eligibility"] = option["status"]
        hybrid["reasons"].extend(notes)
        accounts = monthly_accounts(data, regular, hybrid) if option["active"] is not False else {}
        hybrid.update(regular=regular, accounts=accounts, net=None, gross=None)
        if hybrid["das"] and regular["debit"] is not None:
            hybrid["gross"] = hybrid["das"]["exact"] + regular["debit"]
            nets = [ledger["net"] for ledger in hybrid["accounts"].values()]
            if None not in nets:
                hybrid["net"] = hybrid["das"]["exact"] + sum(nets)
        if option["active"] is True:
            traditional["states"]["eligibility"] = "Contrafactual com opção regular vigente declarada."
        if option["active"] is not True or data["refund"] != "no":
            memory["reasons"].append("A diferença exige opção vigente declarada e confirmação de ausência de vedação por ressarcimento.")
        elif traditional["das"]:
            memory["difference"] = differences(traditional["das"]["exact"], hybrid["net"], traditional["basis"], hybrid["basis"])
        hybrid["states"]["completeness"] = "Completo no perímetro do cenário" if hybrid["net"] is not None else "Parcial"
        memory["states"]["completeness"] = "Comparação condicional" if memory["difference"] is not None else "Parcial"
        for path in (traditional, hybrid):
            if path["states"]["technical"] != "Sucesso":
                memory["states"]["technical"] = path["states"]["technical"]
    return memory
