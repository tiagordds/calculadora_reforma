import json

from django import forms
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from parameters.services import PERIOD, REVISION
from simulation.services import example_inputs, simulate_services
from tax.services import HISTORY_FIELDS
from tax.traditional import history_window
from web.traditional_form import AmountField, MonthField, choice


LABELS = dict(turnover="Receita auferida", wages="Remunerações pagas", pro_labore="Pró-labore pago",
              cpp="CPP recolhida", fgts="FGTS recolhido")


class ServicesForm(forms.Form):
    edition = forms.ChoiceField(choices=[(REVISION, REVISION)], initial=REVISION, widget=forms.HiddenInput)
    period = MonthField(label="Competência da apuração", initial="2027-03")
    opening = MonthField(label="Mês de abertura da empresa")
    origin = choice("Origem dos valores", [("entered", "Históricos informados"), ("synthetic", "Exemplo sintético")], "entered")
    activity = choice("Atividade e local da prestação", [
        ("unknown", "Selecione a atividade"),
        ("software", "Somente software sob encomenda no estabelecimento em Florianópolis"),
        ("other", "Outra atividade, receita mista ou outro local")])
    regime = choice("Regime em março", [("unknown", "Não sei confirmar"),
        ("traditional", "Simples tradicional, sem impedimento"), ("other", "Outra situação")])
    treatment = choice("Condições dos serviços", [("unknown", "Não sei confirmar"),
        ("ordinary", "Todos atendem às condições de ISS e contrato descritas"),
        ("special", "Há retenção, benefício ou outra condição especial")])
    limits = choice("Limites anuais em 2026 e até março de 2027", [("unknown", "Não sei confirmar"),
        ("within", "Dentro do limite global e do sublimite, inclusive proporcional"),
        ("excess", "Há excesso ou impedimento")])
    revenue = AmountField(label="Receita fiscal de março (R$)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.months = history_window(PERIOD)
        for month in self.months:
            for key in HISTORY_FIELDS:
                self.fields[f"{key}_{month}"] = AmountField(label=LABELS[key] + " (R$)")

    def clean(self):
        cleaned = super().clean()
        if set(self.data) - (set(self.fields) | {"csrfmiddlewaretoken"}) or any(
                len(values) != 1 for _, values in self.data.lists()):
            raise forms.ValidationError("Envie somente os campos apresentados, uma vez cada.")
        if cleaned.get("opening") and cleaned.get("period") and cleaned["opening"] > cleaned["period"]:
            self.add_error("opening", "A abertura deve ser anterior ou igual à competência.")
        return cleaned

    def scenario(self):
        data = self.cleaned_data.copy()
        data["history"] = {month: {key: data.pop(f"{key}_{month}") for key in HISTORY_FIELDS} for month in self.months}
        return data


def flatten_history(inputs):
    data = inputs.copy()
    for month, row in data.pop("history").items():
        data.update({f"{key}_{month}": value for key, value in row.items()})
    return data


@require_http_methods(["GET", "HEAD", "POST"])
def services(request):
    post = request.POST if request.method == "POST" else None
    example = (post is not None and post.getlist("example") == ["boundary"]
               and set(post) <= {"example", "csrfmiddlewaretoken"} and len(post.getlist("csrfmiddlewaretoken")) <= 1)
    if example:
        form = ServicesForm(initial=flatten_history(example_inputs()))
    else:
        form = ServicesForm(post)
    memory = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            memory = simulate_services(form.scenario())
            if memory["state"] == "Parâmetros indisponíveis":
                status = 503
        else:
            status = 400
    rows = [(f"{month[5:]}/{month[:4]}", [form[f"{key}_{month}"] for key in HISTORY_FIELDS]) for month in form.months]
    profile = [form[key] for key in ("period", "opening", "activity", "regime", "treatment", "limits", "origin", "revenue")]
    missing = []
    if memory and "history" in memory:
        for key, months in memory["history"]["missing"].items():
            if months:
                missing.append((LABELS[key], ", ".join(f"{m[5:]}/{m[:4]}" for m in months)))
    return render(request, "web/services.html", dict(form=form, profile=profile, rows=rows, example=example,
                  memory=memory, missing=missing, replay=json.dumps(memory, default=str, ensure_ascii=False, indent=2)), status=status)
