import re
from datetime import date
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from parameters.catalog import ACTIVE
from simulation.traditional import PERIOD
from tax.traditional import history_window


class AmountField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(required=False, max_length=18, widget=forms.TextInput(
            attrs={"inputmode": "decimal", "autocomplete": "off", "placeholder": "0,00"}), **kwargs)

    def clean(self, value):
        raw = super().clean(value)
        if not raw:
            return None
        if re.fullmatch(r"[0-9]{1,3}(?:\.[0-9]{3})+(?:,[0-9]{1,2})?", raw):
            raw = raw.replace(".", "")
        if not re.fullmatch(r"[0-9]{1,12}(?:[.,][0-9]{1,2})?", raw):
            raise ValidationError("Use um valor em reais, com até 12 dígitos inteiros e duas casas decimais.")
        return Decimal(raw.replace(",", "."))


class MonthField(forms.RegexField):
    def __init__(self, **kwargs):
        super().__init__(regex=r"^(19|20)[0-9]{2}-(0[1-9]|1[0-2])$", max_length=7,
                         widget=forms.TextInput(attrs={"type": "month"}),
                         error_messages={"invalid": "Informe o ano e o mês, como 2023-01."}, **kwargs)

    def clean(self, value):
        return date.fromisoformat(super().clean(value) + "-01")


def choice(label, pairs, initial=""):
    return forms.ChoiceField(label=label, choices=pairs, initial=initial)


class TraditionalForm(forms.Form):
    edition = forms.ChoiceField(choices=[(ACTIVE, ACTIVE)], initial=ACTIVE, widget=forms.HiddenInput,
                                error_messages={"invalid_choice": "A edição mudou. Reabra a calculadora."})
    period = MonthField(label="Mês da apuração", initial="2027-03")
    opening = MonthField(label="Mês de abertura da empresa")
    activity = choice("Atividade da empresa", [("", "Selecione a atividade"),
        ("retail", "Revenda de caneta esferográfica comum"), ("service", "Serviços"),
        ("industry", "Indústria"), ("mixed", "Atividades mistas"), ("other", "Outra ou desconhecida")])
    place = choice("Local da loja e da entrega", [("", "Selecione o local"),
        ("local", "Ambos em Florianópolis/SC"), ("other", "Outra localidade ou desconhecida")])
    profile = choice("Condições das vendas", [("", "Selecione as condições"),
        ("ordinary", "Todas correspondem ao perfil descrito"), ("special", "Há tratamento especial ou outro fato tributável"),
        ("mixed", "Há outras receitas ou falta segregação"), ("cash", "Há valores a reconhecer do antigo regime de caixa"),
        ("unknown", "Não sei confirmar o perfil")])
    standing = choice("Situação da empresa em março", [
        ("unknown", "Não sei confirmar"), ("traditional", "Optante pelo Simples tradicional"),
        ("impediment", "Impedimento vigente para o Simples"), ("regular", "Optante pelo IBS/CBS regular")], "unknown")
    unit = choice("Período do faturamento histórico", [("monthly", "Média mensal"), ("annual", "Total anual para estimar a média")], "monthly")
    income = AmountField(label="Faturamento histórico (R$)")
    accept_history = forms.ChoiceField(required=False, choices=[("yes", "Aceito estimar os 12 meses pela média.")])
    revenue = AmountField(label="Receita fiscal de março (R$)")
    accept_period = forms.ChoiceField(required=False, choices=[("yes", "Usar a média também para estimar março.")])
    prior_year = AmountField(label="Receita de janeiro a dezembro de 2026 (R$)")
    year_to_date = AmountField(label="Receita de janeiro a março de 2027, incluindo março (R$)")
    mode = forms.ChoiceField(choices=[("estimated", "Estimado"), ("real", "Real")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.months = history_window(PERIOD)
        for m in self.months:
            self.fields["month_" + m] = AmountField(label=f"{m[5:]}/{m[:4]} (R$)")

    def clean(self):
        cleaned = super().clean()
        if set(self.data) - (set(self.fields) | {"csrfmiddlewaretoken"}) or any(
                len(values) != 1 for _, values in self.data.lists()):
            raise ValidationError("Envie somente os campos apresentados, uma vez cada.")
        return cleaned

    def scenario(self):
        data = self.cleaned_data.copy()
        data["history"] = {m: data.pop("month_" + m) for m in self.months}
        for name in ("accept_history", "accept_period"):
            data[name] = data[name] == "yes"
        return data
