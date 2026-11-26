"""Monthly service revenue and paid payroll, for a single domestic activity."""
from decimal import Decimal, localcontext

from tax.traditional import POLICY, assess, das_cents, history_window

PAYROLL = ("wages", "pro_labore", "cpp", "fgts")
HISTORY_FIELDS = ("turnover", *PAYROLL)


def summarize_history(history, period):
    months = history_window(period)
    totals = {}
    missing = {}
    for key in HISTORY_FIELDS:
        series = {month: history.get(month, {}).get(key) for month in months}
        missing[key] = [month for month, value in series.items() if value is None]
        totals[key] = None if missing[key] else sum(series.values())
    payroll = None if any(missing[key] for key in PAYROLL) else sum(totals[key] for key in PAYROLL)
    return dict(months=months, totals=totals, missing=missing, fs12=payroll, rbt12r=totals["turnover"])


def factor_r(payroll, turnover, rules):
    threshold = Decimal(rules["threshold"])
    with localcontext(POLICY):
        if payroll == 0:
            factor = Decimal(rules["zero_payroll_factor"])
            legal_case = "Folha igual a zero (art. 26, § 7º, I ou IV)."
            qualifies = factor >= threshold
        elif turnover == 0:
            factor = Decimal(rules["positive_payroll_zero_revenue_factor"])
            legal_case = "Folha positiva e receita histórica zero (art. 26, § 7º, II)."
            qualifies = factor >= threshold
        else:
            factor = payroll / turnover
            legal_case = "FS12 dividida pela RBT12r (art. 26, § 7º, III)."
            qualifies = payroll >= turnover * threshold
        return dict(ratio=factor, percent=factor * 100, threshold=threshold,
                    payroll_threshold=turnover * threshold, rule=legal_case,
                    annex="III" if qualifies else "V")


def service_das(revenue, basis, band, rules):
    amounts = assess(revenue, basis, band)
    del amounts["annual"]
    cap = Decimal(rules["iss_cap_percent"])
    # Compare before division, even if the ISS rate is extremely close to the cap.
    numerator = amounts["numerator"]
    amounts["iss_capped"] = numerator * Decimal(band["shares"]["ISS"]) > cap * basis
    if amounts["iss_capped"]:
        with localcontext(POLICY):
            # The annex gives explicit weights on the portion remaining after 5% of revenue.
            remainder = numerator * 100 - basis * cap
            for row in amounts["rows"]:
                if row["tax"] == "ISS":
                    rate_numer = cap * basis
                else:
                    rate_numer = remainder * Decimal(rules["capped_remainder_percent"][row["tax"]]) / 100
                row["effective_percent"] = rate_numer / basis
                row["exact"] = revenue * rate_numer / (basis * 100)
                row["displayed"] = das_cents(row["exact"])
                row["share"] = rate_numer / numerator
            amounts["sum_displayed"] = sum(row["displayed"] for row in amounts["rows"])
            amounts["residue"] = amounts["sum_displayed"] - amounts["monthly"]
    return amounts
