from decimal import Decimal, ROUND_HALF_UP

from tax.traditional import CENT, history_window


class InputError(ValueError):
    pass


def build_history(data, period):
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
    revenue = data["revenue"]
    revenue_origin = "informado"
    if revenue is None:
        if average is None or not data["accept_period"]:
            raise InputError("Informe a receita de março ou autorize usar a média informada para esse mês.")
        revenue = average
        revenue_origin = "estimado"
        accepted.append("average_period")
    return dict(series=series, origin=origin, total=sum(series.values()), revenue=revenue,
                revenue_origin=revenue_origin, average=average, accepted=accepted)
