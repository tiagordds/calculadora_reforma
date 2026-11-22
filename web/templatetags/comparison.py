from decimal import Decimal, ROUND_HALF_UP

from django import template

from web.templatetags.traditional import percent, reais

register = template.Library()


@register.filter
def money(value):
    if value is None or value == "":
        return "Em aberto"
    amount = Decimal(value)
    rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount and not rounded:
        return "Entre zero e R$ 0,01" if amount > 0 else "Entre −R$ 0,01 e zero"
    return reais(rounded)


@register.filter
def rate(value):
    return "Em aberto" if value is None or value == "" else percent(value)
