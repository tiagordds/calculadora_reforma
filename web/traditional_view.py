import json

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from simulation.traditional import simulate
from .traditional_form import TraditionalForm


@require_http_methods(["GET", "HEAD", "POST"])
def traditional(request):
    form = TraditionalForm(request.POST if request.method == "POST" else None)
    memory = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            data = form.scenario()
            memory = simulate(data, data["edition"])
            status = {"Entrada inválida": 400, "Parâmetros indisponíveis": 503}.get(memory["states"]["technical"], 200)
        else:
            status = 400
    return render(request, "web/traditional.html", {
        "form": form, "memory": memory,
        "replay": json.dumps(memory, ensure_ascii=False, indent=2, default=str),
        "profile_fields": [form[name] for name in ("period", "opening", "activity", "place", "profile", "standing")],
        "history_fields": [form["month_" + m] for m in form.months],
        "open_real": form.data.get("mode") == "real",
    }, status=status)
