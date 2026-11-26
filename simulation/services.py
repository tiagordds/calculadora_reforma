"""Coordinate C08 without a database, network calls or an item engine."""
import hashlib
from decimal import Decimal
from pathlib import Path

from parameters.catalog import CatalogError
from parameters.services import DIGEST, PERIOD, REVISION, load_rules
from tax.services import factor_r, service_das, summarize_history
from tax.traditional import band_for, history_window, shift_month


def software_digest():
    root = Path(__file__).resolve().parents[1]
    digest = hashlib.sha256()
    for path in ("parameters/catalog.py", "parameters/services.py", "tax/traditional.py",
                 "tax/services.py", "simulation/services.py", "web/traditional_form.py", "web/services.py"):
        digest.update(path.encode() + b"\0" + (root / path).read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


SOFTWARE_HASH = software_digest()


def example_inputs():
    history = {month: dict(turnover="100000", wages="20000", pro_labore="5000", cpp="2000", fgts="1000")
               for month in history_window(PERIOD)}
    return dict(period="2027-03", opening="2023-01", activity="software", regime="traditional",
                treatment="ordinary", limits="within", origin="synthetic", revenue="100000", history=history)


def known_excess(data, sublimit):
    # The reported months establish lower bounds even when the full calendar years are unknown.
    opening = data["opening"]
    prior_limit = sublimit * (13 - opening.month) / 12 if opening.year == 2026 else sublimit
    known = {2026: Decimal(0), 2027: data["revenue"] or Decimal(0)}
    for month, row in data["history"].items():
        known[int(month[:4])] += row["turnover"] or Decimal(0)
    return known[2026] > prior_limit or known[2027] > sublimit


def simulate_services(data):
    memory = dict(software="services-01.1", software_sha256=SOFTWARE_HASH, revision=REVISION, catalog_sha256=DIGEST,
                  inputs=data, state="Parcial", reasons=[], engines=[],
                  scope="Desenvolvimento sob encomenda no estabelecimento em Florianópolis/SC, mercado interno, PA 03/2027.",
                  origin="Hipótese sintética" if data["origin"] == "synthetic" else "Dados informados pelo usuário",
                  validation="Estimativa para ensaio interno. Homologação fiscal pendente.")
    reasons = memory["reasons"]
    if data["period"] != PERIOD:
        reasons.append("A competência habilitada é março de 2027.")
    if data["opening"] > shift_month(PERIOD, -13):
        reasons.append("A empresa precisa estar ao menos no 14º mês de atividade.")
    if data["activity"] != "software":
        reasons.append("Confirme receita exclusiva de programação sob encomenda, realizada no estabelecimento em Florianópolis.")
    if data["regime"] != "traditional":
        reasons.append("Confirme a opção pelo Simples tradicional, sem impedimento, no período.")
    if reasons:
        memory["state"] = "Perfil fora da cobertura ou pendente de confirmação"
        return memory
    try:
        rules = load_rules()
    except CatalogError as exc:
        memory["state"] = "Parâmetros indisponíveis"
        reasons.append(str(exc))
        return memory
    memory.update(sources=rules["sources"], validity=[rules["start"], rules["end"]],
                  rounding="34 dígitos nas divisões. Arredondamento ao centavo, metade para cima e mínimo positivo de R$ 0,01 por valor demonstrado.")
    history = summarize_history(data["history"], PERIOD)
    memory["history"] = history
    if history["fs12"] is None:
        reasons.append("Complete os componentes da folha nos meses em aberto. Informe zero quando conhecido.")
    if history["rbt12r"] is None:
        reasons.append("Complete a receita histórica nos meses em aberto.")
    if data["treatment"] != "ordinary":
        reasons.append("Verifique o local do ISS, retenção, benefícios e condições do contrato antes de incluir o ISS no DAS.")
    if data["limits"] != "within" or known_excess(data, Decimal(rules["annual_sublimit"])):
        reasons.append("Confira os limites e sublimites anuais, inclusive os proporcionais na abertura. Excesso ou situação desconhecida impede estimar o DAS deste perfil.")
    if data["revenue"] is None:
        reasons.append("Informe a receita fiscal de março para calcular o DAS.")
    if history["fs12"] is None or history["rbt12r"] is None:
        return memory
    factor = factor_r(history["fs12"], history["rbt12r"], rules)
    memory["factor"] = factor
    basis = history["rbt12r"] or Decimal(rules["zero_rate_basis"])
    band = band_for(basis, rules["annexes"][factor["annex"]])
    memory.update(rate_basis=basis, band=band)
    if band is None or band["number"] == 6:
        reasons.append("Acima de R$ 3,6 milhões de RBT12, a apuração exige qualificar o recolhimento de ISS e IBS dentro ou fora do DAS.")
    if not reasons:
        memory["amounts"] = service_das(data["revenue"], basis, band, rules)
        memory["state"] = "Estimativa condicionada às premissas informadas"
    return memory
