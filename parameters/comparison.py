from datetime import date

from parameters.catalog import CatalogError, ROOT, number, read_pinned

REVISION = "comparison-04-02"
PREVIOUS = "comparison-04-01"
SIMPLES = "sn-03-02"
RULE_HASH = "6ec3232f39a16389140c2f13434424b2d17184a2ca4dea5a79cd080aa6522b5e"
HASHES = {REVISION: RULE_HASH, PREVIOUS: "74fc3690e2265ac74757ee2889ed88728decb4b79c4813ff5ddf69ebab32364a"}
PREMISE_HASH = "2476cce42a8a2a1c71b64c4c364c834be0c8216aac5b94e0318633f23c4a7fe9"


def premises():
    return read_pinned(ROOT / "comparison_assumptions.json", PREMISE_HASH)


def regular_rules(period, revision=REVISION):
    if revision not in HASHES:
        raise CatalogError("Revisão comparativa desconhecida.")
    rules = read_pinned(ROOT / "data" / (revision + ".json"), HASHES[revision])
    if (rules["revision"] != revision or rules["simples_revision"] != SIMPLES
            or rules["unit"] != "percent"
            or not date.fromisoformat(rules["start"]) <= period <= date.fromisoformat(rules["end"])):
        raise CatalogError("Edição, unidade ou vigência incompatível na apuração regular.")
    return rules


def cbs_rate(rules, hypothesis, accepted):
    if rules["cbs_applicable"] is not None:
        return number(rules["cbs_applicable"]), "Nominal aplicável da edição oficial"
    if accepted and hypothesis is not None:
        return hypothesis, "Nominal hipotética aceita, já considerada a transição"
    return None, "CBS aplicável pendente. Para simular, informe e aceite uma taxa hipotética."
