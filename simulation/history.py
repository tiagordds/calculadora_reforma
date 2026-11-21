from decimal import Decimal, ROUND_HALF_UP

from tax.traditional import CENT, history_window


class InputError(ValueError):
    pass


def build_series(data, period):
    months = history_window(period)
    income = data["income"]
    accepted = []
    average = income
    if income is not None and data["unit"] == "annual":
        average = (income / 12).quantize(CENT, rounding=ROUND_HALF_UP)
    if data["mode"] == "real":
        series = data["history"]
        if set(series) != set(months) or any(v is None for v in series.values()):
            raise InputError("Informe os doze meses da janela. Use zero para mês sem receita.")
        series = {m: series[m] for m in months}
        origin = "informado"
    else:
        if income is None or not data["accept_history"]:
            raise InputError("Para estimar o histórico, informe o faturamento e aceite a hipótese da média.")
        if any(v is not None for v in data["history"].values()):
            raise InputError("Escolha calcular com histórico real para utilizar os meses preenchidos.")
        accepted.append("constant_history")
        if data["unit"] == "annual":
            cents, remainder = divmod(int(income * 100), 12)
            series = {m: Decimal(cents + int(i < remainder)) * CENT for i, m in enumerate(months)}
        else:
            series = dict.fromkeys(months, income)
        origin = "estimado"
    return dict(series=series, origin=origin, total=sum(series.values()), average=average, accepted=accepted)


def build_history(data, period):
    history = build_series(data, period)
    average = history["average"]
    revenue = data["revenue"]
    revenue_origin = "informado"
    if revenue is None:
        if average is None or not data["accept_period"]:
            raise InputError("Informe a receita de março ou autorize usar a média informada para esse mês.")
        revenue = average
        revenue_origin = "estimado"
        history["accepted"].append("average_period")
    return dict(history, revenue=revenue, revenue_origin=revenue_origin)
