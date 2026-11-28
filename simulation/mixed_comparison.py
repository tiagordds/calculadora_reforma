"""Compare two enterprise histories and settle the mixed company's March obligations."""
import hashlib
from decimal import Decimal, localcontext
from pathlib import Path

from parameters import comparison as regular_edition
from parameters.catalog import CatalogError
from simulation.economics import differences
from simulation.mixed import EDITION, GROUPS, PERIOD, SOFTWARE_HASH as MIXED_HASH, consolidate, simulate_mixed
from simulation.service_comparison import SOFTWARE_HASH as SERVICE_HASH
from tax.credits import AccountError, account, acquisition
from tax.option import election
from tax.regular import das_portion, sales
from tax.service_regular import service_turnover
from tax.traditional import POLICY

REVISION = "mixed-hybrid-01"
DESTINATIONS = {"retail": "Comércio", "service": "Serviços", "shared": "Uso compartilhado"}
MOVEMENTS = ("opening", "adjustment", "reversal", "extinguished")
PROFILE = ("period", "opening", "activity", "regime", "limits", "retail_treatment", "service_treatment", "origin")


def software_digest():
    root = Path(__file__).resolve().parents[1]
    digest = hashlib.sha256((MIXED_HASH + SERVICE_HASH).encode())
    for filename in ("simulation/mixed_comparison.py", "web/mixed_comparison.py"):
        digest.update(filename.encode() + b"\0" + (root / filename).read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


SOFTWARE_HASH = software_digest()


def total(values):
    values = list(values)
    return sum(values) if values and None not in values else None


def regular_sales(data, profile, history, rules):
    cbs, origin = regular_edition.cbs_rate(rules, data["cbs_rate"], data["accept_cbs"])
    state, city = (Decimal(rules[key]) for key in ("ibs_state", "ibs_city"))
    rates = dict(cbs_percent=cbs, cbs_origin=origin, state_percent=state, city_percent=city)
    retail_price, service_price = data["retail"], data["service"]
    exclusions = total((data["icms"], data["retail_extra"]))
    retail_notes = []
    if data["retail_treatment"] != "ordinary" or retail_price is None:
        retail_notes.append("Confirme a revenda homogênea local e informe seu preço de março.")
    if exclusions is None or data["retail_exclusion_origin"] == "unknown":
        retail_notes.append("Identifique o ICMS, as demais exclusões comerciais e a origem dos valores.")
    retail = sales(retail_price, None if retail_notes else exclusions, cbs, state, city)
    retail.update(icms=data["icms"], other_exclusions=data["retail_extra"],
                  origin=data["retail_exclusion_origin"], reasons=retail_notes, price=retail_price,
                  revenue_origin="derivada do preço" if retail["revenue"] is not None else "em aberto")

    service_notes = []
    extra = data["service_extra"] if data["service_exclusion_origin"] != "unknown" else None
    iss = data["iss_amount"] if data["iss_basis"] == "document" else None
    share = None
    reported = data["service_reported"]
    if data["destination"] != "local" or data["service_treatment"] != "ordinary" or service_price is None:
        service_notes.append("Confirme as condições do serviço, o preço e o domicílio do adquirente privado em Florianópolis.")
        service = sales(service_price, None, cbs, state, city)
        if data["service_treatment"] == "ordinary" and data["destination"] != "public":
            service["revenue"] = reported
    else:
        if data["iss_basis"] == "proportional":
            # Probe only the historical ISS rate. Recheck the annual screen on the reconstructed turnover below.
            probe = simulate_mixed(dict(profile, history=history, retail=retail["revenue"], service=reported or Decimal(0)))
            amounts = probe["groups"][1].get("amounts")
            if amounts:
                share = next(row["effective_percent"] for row in amounts["rows"] if row["tax"] == "ISS") / 100
        service = service_turnover(service_price, reported, iss, share, extra, cbs, state, city)
        if share is not None and service["revenue"] is not None:
            checked = simulate_mixed(dict(profile, history=history, retail=retail["revenue"], service=service["revenue"]))
            if "amounts" not in checked["groups"][1]:
                share = None
                service = service_turnover(service_price, reported, None, None, extra, cbs, state, city)
        if service["issue"]:
            service_notes.append(service["issue"])
        if service["iss_excluded"] is None:
            service_notes.append("Identifique o ISS excluível nas prestações ou confirme uma hipótese proporcional calculável.")
        if extra is None:
            service_notes.append("Informe as demais exclusões do serviço, inclusive para declarar zero, e sua origem.")
    service.update(iss_share=share, other_exclusions=extra, origin=data["service_exclusion_origin"],
                   revenue_origin=("em aberto" if service["revenue"] is None else
                                   "informada" if reported is not None else "derivada do preço"),
                   reasons=service_notes, price=service_price)
    return rates, {"retail": retail, "service": service}


def retained_assessment(profile, history, regular):
    fiscal = {key: regular[key]["revenue"] for key in GROUPS}
    assessment = simulate_mixed(dict(profile, history=history, **fiscal))
    hybrid = {k: assessment[k] for k in ("history", "factor", "rate_basis", "revenue", "reasons", "parameters_unavailable")}
    hybrid["groups"] = []
    portions = []
    for key, group in zip(GROUPS, assessment["groups"], strict=True):
        row = {k: v for k, v in group.items() if k != "amounts"}
        amounts = group.get("amounts")
        if amounts is not None:
            retained = das_portion(amounts, True)
            row.update(das=retained, iss_capped=amounts.get("iss_capped", False),
                       excluded_rows=[r for r in amounts["rows"] if r["tax"] in ("IBS", "CBS")])
            portions.append(dict(amounts=dict(gross=retained["exact"], monthly=retained["displayed"], rows=retained["rows"])))
        row["regular"] = regular[key]
        hybrid["groups"].append(row)
    hybrid["das"] = consolidate(portions) if len(portions) == len(GROUPS) else None
    return hybrid


def enterprise_accounts(data, regular, notes):
    ledgers = {}
    for tax in ("cbs", "ibs"):
        purchases = []
        for entry in data["acquisitions"].values():
            destination = entry["destination"]
            credit = acquisition(dict(entry, period=PERIOD), tax, PERIOD)
            purchases.append(dict(credit, destination=destination, label=DESTINATIONS[destination],
                                  document=entry["document"]))
        debit = total(row[tax] for row in regular.values())
        credit = Decimal(0) if data["no_acquisitions"] else total(p["appropriated"] for p in purchases)
        movements = [Decimal(0) if data["zero_movements"] else data[tax + "_" + key] for key in MOVEMENTS]
        try:
            ledger = account(debit, credit, *movements, data["account_scope"])
        except AccountError as exc:
            ledger = dict(net=None, debit=debit, error=str(exc))
        ledger["acquisitions"] = purchases
        if ledger["net"] is None:
            notes.append(tax.upper() + " · " + (ledger.get("error") or
                         "Confira débitos, apropriação, movimentos e abrangência da conta empresarial."))
        ledgers[tax] = ledger
    return ledgers


def compare_mixed(data):
    if data["edition"] != REVISION:
        raise CatalogError("Revisão incompatível com a comparação de atividades mistas.")
    with localcontext(POLICY):
        return evaluate(data)


def evaluate(data):
    profile = {key: data[key] for key in PROFILE}
    if profile["regime"] == "member":
        profile["regime"] = "traditional"  # C09 calculates the gross equivalent for each segregated activity.
    if data["destination"] == "public":
        profile["service_treatment"] = "special"
    traditional = simulate_mixed(dict(profile, edition=EDITION, history=data["history"], **{k: data[k] for k in GROUPS}))
    notes = []
    basis = dict(period=data["period"], retail=data["retail"], service=data["service"],
                 final_price=total(data[key] for key in GROUPS), fixed_basket=data["fixed_basket"],
                 retail_quantity=data["retail_quantity"], service_quantity=data["service_quantity"],
                 scope="Obrigação de março após créditos próprios, antes de pagamentos e demais extinções")
    memory = dict(revision=REVISION, software_sha256=SOFTWARE_HASH, inputs=data, traditional=traditional,
                  catalogs={**traditional["editions"], regular_edition.REVISION: regular_edition.RULE_HASH},
                  basis=basis, reasons=notes, hybrid=None, difference=None, guide=None, cash=None, margin=None,
                  engines=[], technical="Sucesso", state="Comparação parcial",
                  document="Estimativa agregada. Correlação preliminar da NFS-e sem combinação documental qualificada.")
    if traditional.get("parameters_unavailable"):
        memory["technical"] = "Parâmetros indisponíveis"
    if "groups" not in traditional:
        notes.extend(traditional["reasons"])
        return memory
    history = data["history"] if data["history_basis"] == "shared" else data["hybrid_history"]
    try:
        rules = regular_edition.regular_rules(PERIOD)
    except CatalogError as exc:
        notes.append(str(exc))
        memory["technical"] = "Parâmetros indisponíveis"
        # Only a reconciled service turnover is independent of the missing regular catalog.
        regular = {key: dict(sales(data[key], None, None, None, None), price=data[key], reasons=[]) for key in GROUPS}
        if profile["service_treatment"] == "ordinary":
            regular["service"]["revenue"] = data["service_reported"]
        memory["hybrid"] = retained_assessment(profile, history, regular)
        return memory
    option = election(data, PERIOD, rules)
    memory.update(option=option, sources=rules["sources"], consulted=rules["consulted"])
    if option["active"] is False:
        notes.append(option["status"])
        return memory
    rates, regular = regular_sales(data, profile, history, rules)
    hybrid = retained_assessment(profile, history, regular)
    memory.update(hybrid=hybrid, rates=rates)
    if rates["cbs_percent"] is None:
        notes.append(rates["cbs_origin"])
    accounts = enterprise_accounts(data, regular, notes)
    if any("error" in ledger for ledger in accounts.values()):
        memory["technical"] = "Entrada inválida"
    if hybrid["parameters_unavailable"]:
        memory["technical"] = "Parâmetros indisponíveis"
    das = hybrid["das"]["gross"] if hybrid["das"] else None
    hybrid.update(accounts=accounts, gross=total([das, *(a["debit"] for a in accounts.values())]),
                  net=total([das, *(a["net"] for a in accounts.values())]))
    if option["active"] is not True or data["refund"] != "no":
        notes.append("A diferença exige opção vigente declarada para o CNPJ e ausência declarada de vedação por ressarcimento.")
    elif not data["fixed_basket"]:
        notes.append("Confirme os mesmos preços, volumes e condições comerciais nas duas trajetórias.")
    elif "amounts" in traditional:
        memory["difference"] = differences(traditional["amounts"]["gross"], hybrid["net"], basis, basis)
        if memory["difference"] is not None:
            memory["state"] = "Comparação condicional completa"
    return memory
