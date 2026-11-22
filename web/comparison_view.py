import json

from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from parameters.catalog import CatalogError
from parameters.comparison import premises
from simulation.comparison import compare
from .comparison_form import ComparisonForm

EXAMPLES = {"zero": "Sem crédito", "middle": "Intermediário", "high": "Alto"}


def example_post(key):
    sample = premises()["example"]
    form = ComparisonForm()
    post = QueryDict(mutable=True)
    for name, field in form.fields.items():
        if field.initial is not None and field.initial is not False:
            post[name] = str(field.initial)
    for name, value in sample.items():
        if name != "cases":
            post[name] = value
    fields = dict(activity="retail", place="local", profile="ordinary", standing="member",
                  accept_history="on", history_basis="shared", accept_cbs="on", exclusion_origin="assumed",
                  supplier="regular", credit_rule="extinction", credit_origin="assumed", credit_evidence="on",
                  event_month="2027-03", account_scope="on", zero_movements="on", option_status="assumed",
                  refund="no", buyer="consumer", example_origin=key, **sample["cases"][key])
    for name, value in fields.items():
        post[name] = value
    return post


def groups(form):
    months = form.months
    sections = [
        ("Vendas e empresa", ["revenue", "quantity", "opening", "activity", "place", "profile", "standing"], True),
        ("Histórico de faturamento", ["mode", "unit", "income", "accept_history", "history_basis"], True),
        ("Históricos próprios e limites anuais", ["month_"+m for m in months] +
         ["hybrid_income"] + ["hybrid_"+m for m in months] +
         ["prior_year", "year_to_date", "hybrid_prior_year", "hybrid_year_to_date"], False),
        ("Composição do preço e CBS", ["exclusions", "exclusion_origin", "cbs_rate", "accept_cbs"], True),
        ("Opção e possibilidade de retorno", ["option_status", "option_date", "cancel_date",
                                              "decision_date", "refund"], False),
        ("Compras e créditos próprios", ["purchases", "purchase_base", "eligible_base", "supplier",
            "credit_origin", "credit_rule", "event_month", "cbs_potential", "ibs_potential", "cbs_credit", "ibs_credit",
            "cbs_transfer", "ibs_transfer", "credit_evidence", "account_scope", "zero_movements"], False),
        ("Saldos e extinções por tributo", [tax+"_"+k for tax in ("cbs", "ibs") for k in
            ("opening", "adjustment", "reversal", "extinguished")], False),
        ("Créditos do cliente", ["buyer", "buyer_document"] +
         [f"buyer_{s}_{t}" for s in ("traditional", "hybrid") for t in ("cbs", "ibs")], False),
    ]
    return [(title, [form[n] for n in names], opened or any(n in form.errors for n in names))
            for title, names, opened in sections]


@require_http_methods(["GET", "HEAD", "POST"])
def comparison(request):
    post = request.POST if request.method == "POST" else None
    status, memory, error = 200, None, ""
    if post is not None and "example" in post:
        if (set(post) <= {"example", "csrfmiddlewaretoken"} and all(len(v) == 1 for _, v in post.lists())
                and post["example"] in EXAMPLES):
            try:
                post = example_post(post["example"])
            except CatalogError as exc:
                error, status = str(exc), 503
        else:
            error, status = "Escolha um exemplo sintético da lista.", 400
    form = ComparisonForm(post)
    if form.is_bound and not error:
        if form.is_valid():
            memory = compare(form.scenario())
            status = {"Entrada inválida": 400, "Parâmetros indisponíveis": 503}.get(memory["states"]["technical"], 200)
        else:
            status = 400
    return render(request, "web/comparison.html", dict(form=form, groups=groups(form), memory=memory,
        replay=json.dumps(memory, indent=2, ensure_ascii=False, default=str), example_error=error,
        examples=EXAMPLES, has_errors=status >= 400), status=status)
