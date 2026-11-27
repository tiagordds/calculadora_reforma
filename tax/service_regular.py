"""Regular base for a month of homogeneous, ordinarily taxed private C08 services."""
from tax.regular import debits_on_base, sales
from tax.traditional import CENT


def service_turnover(price, reported, iss, share, extra, cbs, state, city):
    """H = P - t*B, B = H - ISS - X. Optionally estimate ISS = s*H."""
    result = sales(price, None, cbs, state, city)
    if share is not None:
        if reported is not None:
            iss = reported * share
        elif extra is not None and cbs is not None:
            t = (cbs + state + city) / 100
            iss = share * (price + t * extra) / (1 + t * (1 - share))
    result.update(revenue=reported, iss_excluded=iss, issue=None)
    if iss is None or extra is None:
        return result
    excluded = iss + extra
    if excluded > (reported if reported is not None else price):
        result["issue"] = "As exclusões excedem a receita disponível. Reconcilie o ISS e as demais exclusões."
        return result
    if reported is None:
        result.update(sales(price, excluded, cbs, state, city))
    else:
        debits = debits_on_base(reported - excluded, cbs, state, city)
        if debits["debit"] is not None and (reported + debits["debit"]).quantize(CENT) != price:
            result["issue"] = "A receita fiscal informada e os débitos calculados não reconciliam com o preço ao centavo."
        else:
            result.update(debits)
    return result
