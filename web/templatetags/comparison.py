from decimal import Decimal, ROUND_HALF_UP

from django import template

from web.templatetags.traditional import percent, reais

register = template.Library()


@register.filter
def money(value):
    if value is None or value == "":
        return "Em aberto"
    return reais(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


@register.filter
def rate(value):
    return "Em aberto" if value is None or value == "" else percent(value)
