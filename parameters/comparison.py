from datetime import date

from parameters.catalog import CatalogError, ROOT, number, read_pinned

REVISION = "comparison-04-01"
SIMPLES = "sn-03-02"
RULE_HASH = "74fc3690e2265ac74757ee2889ed88728decb4b79c4813ff5ddf69ebab32364a"
PREMISE_HASH = "2476cce42a8a2a1c71b64c4c364c834be0c8216aac5b94e0318633f23c4a7fe9"


def premises():
    return read_pinned(ROOT / "comparison_assumptions.json", PREMISE_HASH)


def regular_rules(period):
    rules = read_pinned(ROOT / "data" / (REVISION + ".json"), RULE_HASH)
    if (rules["revision"] != REVISION or rules["simples_revision"] != SIMPLES
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
