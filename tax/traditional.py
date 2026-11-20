"""Monthly enterprise arithmetic. Percentages in tables are expressed per hundred."""
from datetime import date
from decimal import Context, Decimal, ROUND_HALF_UP, localcontext

CENT = Decimal("0.01")
POLICY = Context(prec=34, rounding=ROUND_HALF_UP)


def shift_month(month, offset):
    year, index = divmod(month.year * 12 + month.month - 1 + offset, 12)
    return date(year, index + 1, 1)


def history_window(period):
    return tuple(shift_month(period, i).strftime("%Y-%m") for i in range(-13, -1))


def das_cents(value):
    cents = value.quantize(CENT, rounding=ROUND_HALF_UP)
    return CENT if value > 0 and cents == 0 else cents


def band_for(total, bands):
    return next((b for b in bands if Decimal(b["above"]) < total <= Decimal(b["through"])), None)


def assess(revenue, total, band):
    with localcontext(POLICY):
        numerator = total * Decimal(band["nominal"]) / 100 - Decimal(band["deduction"])
        effective = numerator / total
        # Multiply before dividing to preserve exact half-cent ties in monetary values.
        gross = revenue * numerator / total
        rows = []
        for tax, raw_share in band["shares"].items():
            share = Decimal(raw_share)
            exact = revenue * numerator * share / (total * 100)
            rows.append(dict(tax=tax, share=share, effective_percent=numerator * share / total,
                             exact=exact, displayed=das_cents(exact)))
        monthly = das_cents(gross)
        sum_displayed = sum(row["displayed"] for row in rows)
        return dict(numerator=numerator, effective_percent=effective * 100, gross=gross,
                    monthly=monthly, rows=rows, sum_displayed=sum_displayed,
                    residue=sum_displayed - monthly, annual=monthly * 12)


def annual_excesses(amount, year, opening, period, parameters, before_period=None):
    """Describe both thresholds, even when the same turnover exceeds both."""
    months = 13 - opening.month if opening.year == year else 12
    findings = []
    local_effect = ("impedimento do recolhimento unificado de ICMS e ISS (verificar também o IBS a partir de 2027)"
                    if year == 2026 else "recolhimento de IBS, ICMS e ISS fora do DAS")
    for key, effect in (("annual_sublimit", local_effect),
                        ("annual_limit", "exclusão do Simples Nacional")):
        threshold = Decimal(parameters[key]) * months / 12
        if amount <= threshold:
            continue
        high = amount > threshold * (1 + Decimal(parameters["excess_margin"]) / 100)
        if not high:
            start = f"janeiro de {year + 1}"
        elif opening.year == year:
            start = f"início da atividade em {opening:%m/%Y} (efeito retroativo)"
        elif year == period.year and before_period is not None and before_period <= threshold * (
                1 + Decimal(parameters["excess_margin"]) / 100):
            start = shift_month(period, 1).strftime("%m/%Y")
        else:
            start = "mês seguinte à ultrapassagem de 20% (conferir o primeiro mês na escrituração)"
        findings.append(dict(year=year, kind=key, threshold=threshold, amount=amount,
                             excess=amount-threshold, above_twenty=high, effect=effect, start=start))
    return findings
