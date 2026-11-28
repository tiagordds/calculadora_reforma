import json

from django import forms
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from simulation.mixed import EDITION, GROUPS, PERIOD, example_inputs, simulate_mixed
from tax.services import PAYROLL
from tax.traditional import history_window
from web.services import LABELS as SERVICE_LABELS, ServicesForm, flatten_history
from web.traditional_form import AmountField, choice

ORIGINS = [("entered", "Informado pela empresa"), ("estimated", "Estimado"), ("synthetic", "Exemplo sintético")]
LABELS = {**SERVICE_LABELS, "service": "Receita de serviços", "retail": "Receita comercial"}
HISTORY = (*GROUPS, *PAYROLL, "origin")
CONDITIONS = [("unknown", "Não sei confirmar"), ("ordinary", "Atende às condições descritas"),
              ("special", "Há tratamento especial ou pendência")]


class MixedForm(forms.Form):
    edition = forms.ChoiceField(choices=[(EDITION, EDITION)], initial=EDITION, widget=forms.HiddenInput)
    period = ServicesForm.base_fields["period"]
    opening = ServicesForm.base_fields["opening"]
    activity = choice("Atividades do estabelecimento", [("unknown", "Selecione as atividades"),
        ("mixed", "Revenda de canetas e software sob encomenda em Florianópolis"), ("other", "Outro perfil")])
    regime = ServicesForm.base_fields["regime"]
    limits = ServicesForm.base_fields["limits"]
    retail_treatment = choice("Condições da revenda", CONDITIONS)
    service_treatment = choice("Condições do serviço", CONDITIONS)
    retail = AmountField(label="Receita comercial de março (R$)")
    service = AmountField(label="Receita de serviços de março (R$)")
    origin = choice("Origem das receitas de março", ORIGINS, "entered")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.months = history_window(PERIOD)
        for month in self.months:
            for key in (*GROUPS, *PAYROLL):
                self.fields[f"{key}_{month}"] = AmountField(label=LABELS[key] + " (R$)")
            self.fields[f"origin_{month}"] = choice("Origem dos dados do mês", ORIGINS, "entered")

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
        data["history"] = {month: {key: data.pop(f"{key}_{month}") for key in HISTORY} for month in self.months}
        return data


@require_http_methods(["GET", "HEAD", "POST"])
def mixed(request):
    post = request.POST if request.method == "POST" else None
    example = (post is not None and post.getlist("example") == ["c09"]
               and set(post) <= {"example", "csrfmiddlewaretoken"} and len(post.getlist("csrfmiddlewaretoken")) <= 1)
    form = MixedForm(initial=flatten_history(example_inputs())) if example else MixedForm(post)
    memory = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            memory = simulate_mixed(form.scenario())
            if memory.get("parameters_unavailable"):
                status = 503
        else:
            status = 400
    months = [(f"{month[5:]}/{month[:4]}", [form[f"{key}_{month}"] for key in HISTORY]) for month in form.months]
    missing = []
    if memory:
        for month, row in memory["history"]["series"].items():
            if row["missing"]:
                missing.append((f"{month[5:]}/{month[:4]}", ", ".join(LABELS[key] for key in row["missing"])))
    return render(request, "web/mixed.html", dict(form=form, profile=[form[key] for key in MixedForm.base_fields
                  if key != "edition"], months=months, example=example, memory=memory, missing=missing,
                  replay=json.dumps(memory, default=str, ensure_ascii=False, indent=2)), status=status)
