"""Monthly homogeneous retail sales. Rates at this boundary are percentages."""
from tax.traditional import CENT, das_cents


def sales(price, exclusions, cbs_percent, state_percent, city_percent):
    result = dict(base=None, revenue=None, cbs=None, ibs=None, state=None, city=None,
                  debit=None, ibs_rounding_residue=None)
    if exclusions is None or cbs_percent is None:
        return result
    base = (price - exclusions) / (1 + (cbs_percent + state_percent + city_percent) / 100)
    state, city = base * state_percent / 100, base * city_percent / 100
    cbs = base * cbs_percent / 100
    debit = state + city + cbs
    return dict(base=base, revenue=price-debit, cbs=cbs, ibs=state+city, state=state,
                city=city, debit=debit, ibs_rounding_residue=(
                    state.quantize(CENT) + city.quantize(CENT) - (state+city).quantize(CENT)))


def das_portion(assessment, hybrid):
    rows = [row for row in assessment["rows"] if not hybrid or row["tax"] not in ("CBS", "IBS")]
    exact = sum(row["exact"] for row in rows) if hybrid else assessment["gross"]
    displayed = das_cents(exact)
    return dict(rows=rows, exact=exact, displayed=displayed,
                effective_percent=sum(row["effective_percent"] for row in rows),
                global_percent=assessment["effective_percent"],
                residue=sum(row["displayed"] for row in rows) - displayed)
