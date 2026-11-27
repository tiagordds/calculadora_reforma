import json
from copy import deepcopy
from datetime import date

from django import forms
from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from simulation.service_comparison import REVISION, compare_services
from simulation.services import example_inputs
from tax.services import HISTORY_FIELDS
from web.comparison_form import ComparisonForm, validate_regular_fields
from web.services import LABELS, ServicesForm, flatten_history
from web.traditional_form import AmountField, choice

CREDIT_FIELDS = ("supplier", "credit_origin", "credit_rule", "event_month", "credit_evidence",
                 "account_scope", "zero_movements")
MOVEMENTS = ("opening", "adjustment", "reversal", "extinguished")
TAX_FIELDS = tuple(f"{tax}_{key}" for tax in ("cbs", "ibs")
                   for key in ("potential", "credit", "transfer", *MOVEMENTS))
OPTION_FIELDS = ("option_status", "option_date", "cancel_date", "decision_date", "refund")
REGULAR_FIELDS = ("quantity", "cbs_rate", "accept_cbs", "exclusions", "exclusion_origin",
                  *OPTION_FIELDS, *CREDIT_FIELDS, *TAX_FIELDS)


class ServiceComparisonForm(ServicesForm):
    edition = forms.ChoiceField(choices=[(REVISION, REVISION)], initial=REVISION, widget=forms.HiddenInput)
    regime = choice("Situação da empresa nas duas trajetórias", [
        ("unknown", "Não sei confirmar"), ("member", "Optante do Simples sem impedimento declarado"),
        ("other", "Há impedimento ou outro regime")], "unknown")
    destination = choice("Local da operação para IBS e CBS", [
        ("unknown", "A confirmar"), ("local", "Domicílio aplicável do cliente privado em Florianópolis"),
        ("other", "Cliente privado em outro destino"), ("public", "Cliente público")], "unknown")
    history_basis = choice("Origem do histórico híbrido", [
        ("own", "Informar receitas e folha próprias"), ("shared", "Aceito usar as mesmas doze receitas e os mesmos componentes da folha")], "own")
    iss_basis = choice("ISS incidente a excluir da base regular", [
        ("unknown", "Ainda a confirmar"), ("document", "Valor identificado nas prestações do mês"),
        ("proportional", "Aceito estimar o ISS pela parcela efetiva do híbrido sobre a receita fiscal")], "unknown")
    iss_amount = AmountField(label="ISS identificado nas prestações, se conhecido (R$)")
    hybrid_revenue = AmountField(label="Receita fiscal híbrida de março já conciliada, se conhecida (R$)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        commercial = ComparisonForm()
        for key in REGULAR_FIELDS:
            self.fields[key] = deepcopy(commercial.fields[key])
        self.fields["revenue"].label = "Preço final dos serviços de março, igual nas duas trajetórias (R$)"
        self.fields["revenue"].required = True
        self.fields["quantity"].label = "Quantidade de serviços no mês, comum às duas trajetórias (se conhecida)"
        self.fields["cbs_rate"].label = "CBS hipotética aplicável após a transição (%)"
        self.fields["exclusions"].label = "Outras exclusões legais da base regular já incluídas no preço, além do ISS (R$)"
        self.fields["limits"].label = "Limites anuais nas duas trajetórias em 2026 e até março de 2027"
        for month in self.months:
            for key in HISTORY_FIELDS:
                self.fields[f"hybrid_{key}_{month}"] = AmountField(label=LABELS[key] + " do híbrido (R$)")

    def clean(self):
        data = super().clean()
        validate_regular_fields(self, data)
        if data.get("history_basis") == "shared" and any(data.get(f"hybrid_{k}_{m}") is not None
                for m in self.months for k in HISTORY_FIELDS):
            self.add_error("history_basis", "Há dados próprios do híbrido. Selecione o histórico próprio ou remova esses valores.")
        if data.get("quantity") == 0 and data.get("revenue"):
            self.add_error("quantity", "Informe uma quantidade positiva ou deixe em aberto.")
        if data.get("iss_amount") is not None and data.get("iss_basis") != "document":
            self.add_error("iss_amount", "Selecione o ISS identificado para usar esse valor.")
        if None not in (data.get("hybrid_revenue"), data.get("revenue")) and data["hybrid_revenue"] > data["revenue"]:
            self.add_error("hybrid_revenue", "A receita fiscal híbrida supera o preço final.")
        if data.get("iss_amount") is not None and data.get("revenue") is not None:
            if data["iss_amount"] + (data.get("exclusions") or 0) > data["revenue"]:
                self.add_error("iss_amount", "O ISS e as demais exclusões superam o preço final.")
        for tax in ("ibs", "cbs"):
            if data.get(tax + "_credit") and data.get("supplier") != "regular":
                self.add_error(tax + "_credit", "Identifique o fornecedor regular deste destaque.")
            if data.get(tax + "_transfer") and data.get("supplier") != "simples":
                self.add_error(tax + "_transfer", "Identifique o fornecedor do Simples deste valor transferível.")
        return data

    def scenario(self):
        data = super().scenario()
        data["hybrid_history"] = {month: {key: data.pop(f"hybrid_{key}_{month}") for key in HISTORY_FIELDS}
                                  for month in self.months}
        if data["event_month"]:
            data["event_month"] = date.fromisoformat(data["event_month"] + "-01")
        else:
            data["event_month"] = None
        return data


def sample():
    base = example_inputs()
    base["history"]["2027-01"]["wages"] = "19999.99"
    data = flatten_history(base)
    for month, row in base["history"].items():
        for key, value in row.items():
            data[f"hybrid_{key}_{month}"] = value
    data.update(edition=REVISION, regime="member", destination="local", history_basis="own",
                quantity="10", iss_basis="proportional", cbs_rate="10", accept_cbs="on", exclusions="0",
                exclusion_origin="assumed", option_status="active", option_date="2026-10-15",
                decision_date="2027-03-01", refund="no", supplier="regular", credit_origin="assumed",
                credit_rule="extinction", event_month="2027-03", credit_evidence="on", account_scope="on",
                zero_movements="on", cbs_credit="0", ibs_credit="0")
    data["hybrid_turnover_2027-01"] = "90000"
    return data


def replay_post(inputs):
    fields = flatten_history(inputs)
    for month, row in fields.pop("hybrid_history").items():
        fields.update({f"hybrid_{key}_{month}": value for key, value in row.items()})
    post = QueryDict(mutable=True)
    for key, value in fields.items():
        if key in ("period", "opening", "event_month") and value is not None:
            if not value.endswith("-01"):
                raise ValueError("Competência inválida.")
            value = value[:7]
        if isinstance(value, bool):
            value = "on" if value else ""
        post[key] = "" if value is None else value
    return post


@require_http_methods(["GET", "HEAD", "POST"])
def service_comparison(request):
    post = request.POST if request.method == "POST" else None
    if (post is not None and set(post) <= {"example", "csrfmiddlewaretoken"}
            and post.getlist("example") == ["boundary"] and len(post.getlist("csrfmiddlewaretoken")) <= 1):
        post = QueryDict(mutable=True)
        post.update(sample())
    initial = None
    if post is not None and post.getlist("carry") == ["services"]:
        carried = post.copy()
        del carried["carry"]
        original = ServicesForm(carried)
        if original.is_valid():
            initial = carried.dict()
            initial.update(edition=REVISION, regime="member" if initial["regime"] == "traditional" else initial["regime"])
            post = None
    form = ServiceComparisonForm(post, initial=initial)
    memory = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            memory = compare_services(form.scenario())
            status = {"Entrada inválida": 400, "Parâmetros indisponíveis": 503}.get(memory["states"]["technical"], 200)
        else:
            status = 400
    groups = [
        ("Empresa e prestações", ("revenue", "quantity", "period", "opening", "activity", "regime", "treatment",
                                 "destination", "limits", "origin", "history_basis")),
        ("Base e taxas regulares", ("hybrid_revenue", "iss_basis", "iss_amount", "exclusions", "exclusion_origin", "cbs_rate", "accept_cbs")),
        ("Opção pelo regime regular", OPTION_FIELDS),
        ("Créditos e movimentos de março", (*CREDIT_FIELDS, *TAX_FIELDS)),
    ]
    sections = [(name, [form[k] for k in keys], i == 0 or any(k in form.errors for k in keys))
                for i, (name, keys) in enumerate(groups)]
    histories = []
    for title, prefix in (("Tradicional", ""), ("Híbrido", "hybrid_")):
        rows = [(m, [form[f"{prefix}{k}_{m}"] for k in HISTORY_FIELDS]) for m in form.months]
        histories.append((title, rows, any(f.errors for _, fields in rows for f in fields)))
    paths = [("Tradicional", memory["traditional"]), ("Híbrido", memory["hybrid"])] if memory else []
    return render(request, "web/service_comparison.html", dict(form=form, sections=sections, histories=histories,
                  paths=paths, memory=memory, replay=json.dumps(memory, indent=2, default=str, ensure_ascii=False)), status=status)
