from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def reais(value):
    return "R$ " + format(Decimal(value), ",.2f").translate(str.maketrans(",.", ".,"))


@register.filter
def percent(value):
    digits = format(Decimal(value), ".9f").rstrip("0").rstrip(".")
    return digits.replace(".", ",") + "%"
