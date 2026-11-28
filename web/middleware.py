from time import monotonic

from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers

from adapters.regular import BUDGET

OPERATION_PATH = "/operacao/caneta/"
TRADITIONAL_PATH = "/simples/tradicional/"
COMPARISON_PATH = "/simples/comparar/"
SERVICES_PATH = "/simples/servicos/"
MIXED_PATH = "/simples/atividades-mistas/"
MIXED_COMPARISON_PATH = MIXED_PATH + "comparar/"
SERVICE_COMPARISON_PATH = SERVICES_PATH + "comparar/"


def private_operation(get_response):
    def middleware(request):
        if request.path not in (OPERATION_PATH, TRADITIONAL_PATH, COMPARISON_PATH, SERVICES_PATH,
                                SERVICE_COMPARISON_PATH, MIXED_PATH, MIXED_COMPARISON_PATH):
            return get_response(request)
        if request.path == OPERATION_PATH:
            request.calculation_deadline = monotonic() + BUDGET - 0.15
        length = request.META.get("CONTENT_LENGTH") or "0"
        if not length.isascii() or not length.isdecimal() or len(length) > 18:
            response = HttpResponse("Tamanho de formulário inválido.", status=400)
        elif request.META.get("QUERY_STRING"):
            response = HttpResponse("Abra a operação sem parâmetros na URL.", status=400)
        elif request.method == "POST" and int(length) > 65536:
            response = HttpResponse("O formulário excede o tamanho permitido.", status=413)
        elif request.method == "POST" and request.content_type != "application/x-www-form-urlencoded":
            response = HttpResponse("Envie a confirmação pelo formulário da operação.", status=415)
        else:
            response = get_response(request)
        add_never_cache_headers(response)
        response["X-Robots-Tag"] = "noindex, nofollow"
        response["Referrer-Policy"] = "same-origin"
        return response
    return middleware
