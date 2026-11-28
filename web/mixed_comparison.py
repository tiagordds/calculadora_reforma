import json
import re
from copy import deepcopy
from datetime import date

from django import forms
from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from simulation.mixed import GROUPS, PERIOD, example_inputs
from simulation.mixed_comparison import DESTINATIONS, MOVEMENTS, REVISION, compare_mixed
from web.comparison_form import ComparisonForm, flag, validate_regular_fields
from web.mixed import HISTORY, MixedForm
from web.service_comparison import OPTION_FIELDS, ServiceComparisonForm, replay_post as history_post
from web.services import flatten_history
from web.traditional_form import AmountField

ACCOUNT_FIELDS = ("account_scope", "zero_movements", *(f"{tax}_{key}" for tax in ("cbs", "ibs") for key in MOVEMENTS))
PURCHASE_FIELDS = ("supplier", "credit_origin", "credit_rule", "event_month", "credit_evidence",
                   *(f"{tax}_{key}" for tax in ("cbs", "ibs") for key in ("potential", "credit", "transfer")))


class AcquisitionForm(forms.Form):
    document = forms.RegexField(label="Referência local única do documento (apelido, sem dados pessoais)",
                                regex=r"^[A-Za-z0-9][A-Za-z0-9_-]{0,31}$", max_length=32)

    def __init__(self, post, destination, commercial):
        super().__init__(post, prefix=destination, empty_permitted=True, use_required_attribute=False)
        for key in PURCHASE_FIELDS:
            field = deepcopy(commercial.fields[key])
            if isinstance(field, forms.ChoiceField):
                field.choices = [("", "Selecione se houver aquisição"), *field.choices]
                field.initial = ""
            self.fields[key] = field

    def clean(self):
        data = super().clean()
        # Acquisitions belong to March for this profile, even if appropriation occurs later.
        validate_regular_fields(self, dict(data, period=PERIOD))
        if self.data.get(self.add_prefix("credit_evidence")) not in (None, "", "on"):
            self.add_error("credit_evidence", "Confirmação documental inválida.")
        for tax in ("cbs", "ibs"):
            for kind, supplier in (("credit", "regular"), ("transfer", "simples")):
                if data.get(f"{tax}_{kind}") and data.get("supplier") != supplier:
                    self.add_error(f"{tax}_{kind}", "Confira o valor com o tratamento declarado do fornecedor.")
        return data

    def scenario(self):
        row = self.cleaned_data.copy()
        row["destination"] = self.prefix.split("_")[0]
        month = row["event_month"]
        row["event_month"] = date.fromisoformat(month + "-01") if month else None
        return row


class MixedComparisonForm(MixedForm):
    edition = forms.ChoiceField(choices=[(REVISION, REVISION)], initial=REVISION, widget=forms.HiddenInput)
    regime = ServiceComparisonForm.base_fields["regime"]
    destination = ServiceComparisonForm.base_fields["destination"]
    history_basis = ServiceComparisonForm.base_fields["history_basis"]
    iss_basis = ServiceComparisonForm.base_fields["iss_basis"]
    iss_amount = ServiceComparisonForm.base_fields["iss_amount"]
    service_reported = AmountField(label="Receita fiscal híbrida dos serviços já conciliada, se conhecida (R$)")
    icms = AmountField(label="ICMS incidente excluível nas vendas (R$)")
    retail_extra = AmountField(label="Outras exclusões comerciais além do ICMS (R$)")
    service_extra = AmountField(label="Outras exclusões dos serviços além do ISS (R$)")
    fixed_basket = flag("Confirmo os mesmos preços finais, volumes, operações e condições comerciais por atividade.")
    no_acquisitions = flag("Declaro que não há créditos de aquisições a apropriar em março nas duas contas.")

    def __init__(self, data=None, *, initial=None, add_purchase=None):
        commercial = ComparisonForm()
        slots = list(DESTINATIONS)
        for name in data or ():
            match = re.fullmatch(r"((?:retail|service|shared)_[1-9][0-9]*)-document", name)
            if match:
                slots.append(match[1])
        if add_purchase:
            index = 1
            while f"{add_purchase}_{index}" in slots:
                index += 1
            slots.append(f"{add_purchase}_{index}")
        self.purchases = {key: AcquisitionForm(data, key, commercial) for key in slots}
        if data is not None:
            data = data.copy()
            for purchase in self.purchases.values():
                for key in purchase.fields:
                    name = purchase.add_prefix(key)
                    if len(data.getlist(name)) == 1:
                        del data[name]  # Repeated or unexpected keys reach MixedForm's rejection.
        super().__init__(data, initial=initial)
        for key in (*OPTION_FIELDS, *ACCOUNT_FIELDS, "cbs_rate", "accept_cbs"):
            self.fields[key] = deepcopy(commercial.fields[key])
        self.fields["cbs_rate"].label = "CBS hipotética após a transição, para os dois grupos (%)"
        self.fields["limits"].label = "Limites anuais confirmados para as duas trajetórias"
        self.fields["history_basis"].choices = [
            ("own", "Informar histórico fiscal e folha próprios do híbrido"),
            ("shared", "Aceito repetir as duas receitas e cada componente de folha dos doze meses")]
        for key in GROUPS:
            label = DESTINATIONS[key]
            self.fields[key].label = "Preço final de março · " + label + " (R$)"
            self.fields[key + "_quantity"] = deepcopy(commercial.fields["quantity"])
            self.fields[key + "_quantity"].label = "Quantidade comum nas duas trajetórias · " + label + " (se conhecida)"
            self.fields[key + "_exclusion_origin"] = deepcopy(commercial.fields["exclusion_origin"])
        for month in self.months:
            for key in HISTORY:
                self.fields[f"hybrid_{key}_{month}"] = deepcopy(self.fields[f"{key}_{month}"])

    def clean(self):
        data = super().clean()
        validate_regular_fields(self, data)
        for key in ("option_date", "decision_date"):
            day = data.get(key)
            if day and day.year == date.max.year and day.month in (3, 9):
                self.add_error(key, "A data ultrapassa o calendário disponível para calcular o semestre seguinte.")
        refs = set()
        for purchase in self.purchases.values():
            if not purchase.is_valid():
                self.add_error(None, "Revise os dados da aquisição.")
            elif purchase.has_changed():
                ref = purchase.cleaned_data["document"].casefold()
                if ref in refs:
                    purchase.add_error("document", "Este documento já foi incluído em outra destinação.")
                    self.add_error(None, "Cada aquisição deve aparecer uma única vez.")
                refs.add(ref)
        if data.get("no_acquisitions") and refs:
            self.add_error("no_acquisitions", "Há documentos na simulação. Informe os créditos de cada um.")
        if data.get("history_basis") == "shared" and any(data.get(f"hybrid_{key}_{month}") is not None
                for key in HISTORY if key != "origin" for month in self.months):
            self.add_error("history_basis", "Há valores próprios do híbrido. Use o histórico próprio ou limpe os valores.")
        for group in GROUPS:
            if data.get(group) and data.get(group + "_quantity") == 0:
                self.add_error(group + "_quantity", "A quantidade deve ser positiva para preço positivo.")
        if data.get("iss_amount") is not None and data.get("iss_basis") != "document":
            self.add_error("iss_amount", "Selecione ISS identificado nas prestações para usar esse valor.")
        for price, parts in (("retail", ("icms", "retail_extra")), ("service", ("iss_amount", "service_extra")),
                             ("service", ("service_reported",))):
            if data.get(price) is not None and sum(data.get(key) or 0 for key in parts) > data[price]:
                self.add_error(parts[-1], "O valor informado supera o preço final da atividade.")
        return data

    def scenario(self):
        data = super().scenario()
        data["hybrid_history"] = {month: {key: data.pop(f"hybrid_{key}_{month}") for key in HISTORY}
                                  for month in self.months}
        data["acquisitions"] = {key: form.scenario() for key, form in self.purchases.items() if form.has_changed()}
        return data


def sample():
    base = example_inputs()
    base["history"]["2027-01"]["wages"] = "19999.99"
    fields = flatten_history(base)
    for month, row in base["history"].items():
        fields.update({f"hybrid_{k}_{month}": v for k, v in row.items()})
    fields.update(edition=REVISION, regime="member", destination="local", history_basis="own",
                  fixed_basket="on", retail_quantity="6000", service_quantity="4",
                  icms="4950", retail_extra="0", retail_exclusion_origin="assumed",
                  iss_basis="document", iss_amount="1463", service_extra="2", service_exclusion_origin="assumed",
                  cbs_rate="10", accept_cbs="on", option_status="active", option_date="2026-10-15",
                  decision_date="2027-03-01", refund="no", account_scope="on", zero_movements="on")
    fields["hybrid_retail_2027-01"] = "50000"
    fields.update({"shared-document": "EXEMPLO-01", "shared-supplier": "regular", "shared-credit_origin": "assumed",
                   "shared-credit_rule": "extinction", "shared-event_month": "2027-03", "shared-credit_evidence": "on",
                   "shared-cbs_credit": "0", "shared-ibs_credit": "0"})
    return fields


def replay_post(inputs):
    data = inputs.copy()
    acquisitions = data.pop("acquisitions")
    post = history_post(data)
    for destination, purchase in acquisitions.items():
        for key, value in purchase.items():
            if key == "destination":
                continue  # The form derives this from the destination of the document slot.
            if key == "event_month" and value is not None:
                if not value.endswith("-01"):
                    raise ValueError("Competência de apropriação inválida.")
                value = value[:7]
            if isinstance(value, bool):
                value = "on" if value else ""
            post[f"{destination}-{key}"] = "" if value is None else value
    return post


@require_http_methods(["GET", "HEAD", "POST"])
def mixed_comparison(request):
    post = request.POST if request.method == "POST" else None
    initial = None
    add_purchase = None
    if (post is not None and post.getlist("example") == ["mixed"] and set(post) <= {"example", "csrfmiddlewaretoken"}
            and len(post.getlist("csrfmiddlewaretoken")) <= 1):
        post = QueryDict(mutable=True)
        post.update(sample())
    elif post is not None and post.getlist("carry") == ["mixed"]:
        carried = post.copy()
        del carried["carry"]
        if MixedForm(carried).is_valid():
            initial = carried.dict()
            initial.update(edition=REVISION, regime="member" if initial["regime"] == "traditional" else initial["regime"])
            post = None
    elif post is not None and len(post.getlist("add_purchase")) == 1 and post["add_purchase"] in DESTINATIONS:
        post = post.copy()
        add_purchase = post.pop("add_purchase")[0]
    form = MixedComparisonForm(post, initial=initial, add_purchase=add_purchase)
    memory = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            if not add_purchase:
                memory = compare_mixed(form.scenario())
                status = {"Entrada inválida": 400, "Parâmetros indisponíveis": 503}.get(memory["technical"], 200)
        else:
            status = 400
    sections = [
        ("Empresa e operações de março", ("retail", "service", "retail_quantity", "service_quantity", "fixed_basket",
            "period", "opening", "activity", "regime", "limits", "retail_treatment", "service_treatment",
            "origin", "destination", "history_basis")),
        ("Exclusões e alíquotas", ("icms", "retail_extra", "retail_exclusion_origin", "iss_basis", "iss_amount",
            "service_extra", "service_exclusion_origin", "service_reported", "cbs_rate", "accept_cbs")),
        ("Opção empresarial", OPTION_FIELDS), ("Contas empresariais de CBS e IBS", ("no_acquisitions", *ACCOUNT_FIELDS))]
    sections = [(name, [form[k] for k in keys], i == 0 or any(k in form.errors for k in keys))
                for i, (name, keys) in enumerate(sections)]
    histories = []
    for title, prefix in (("Tradicional", ""), ("Híbrido", "hybrid_")):
        rows = [(m, [form[f"{prefix}{k}_{m}"] for k in HISTORY]) for m in form.months]
        histories.append((title, rows, any(f.errors for _, fields in rows for f in fields)))
    return render(request, "web/mixed_comparison.html", dict(form=form, memory=memory, sections=sections,
                  histories=histories, destinations=DESTINATIONS,
                  purchases=[(DESTINATIONS[k.split("_")[0]], v) for k, v in form.purchases.items()],
                  replay=json.dumps(memory, indent=2, ensure_ascii=False, default=str)), status=status)
