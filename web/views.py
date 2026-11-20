from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe

from simulation.service import Outcome, simulate_pen
from .forms import PenForm


@require_safe
def home(request):
    return render(request, "web/home.html")


def csrf_failure(request, reason=""):
    return HttpResponseForbidden("A confirmação de segurança expirou ou é inválida. Abra o formulário novamente.")


@require_http_methods(["GET", "HEAD", "POST"])
def pen(request):
    form = PenForm(request.POST if request.method == "POST" else None)
    outcome = None
    if form.is_bound:
        if form.is_valid():
            outcome = simulate_pen(confirmed=form.cleaned_data["confirm_cbs"] == "yes",
                                   deadline=request.calculation_deadline)
        else:
            outcome = Outcome("Entrada inválida", error="Revise a confirmação abaixo.", status=400)
    return render(request, "web/pen.html", {"form": form, "outcome": outcome},
                  status=outcome.status if outcome else 200)
