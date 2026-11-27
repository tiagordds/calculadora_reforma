from django.urls import path

from web.comparison_view import comparison
from web.middleware import COMPARISON_PATH, OPERATION_PATH, SERVICES_PATH, TRADITIONAL_PATH
from web.middleware import SERVICE_COMPARISON_PATH
from web.service_comparison import service_comparison
from web.services import services
from web.traditional_view import traditional
from web.views import home, pen


urlpatterns = [
    path("", home, name="home"),
    path(OPERATION_PATH.lstrip("/"), pen, name="pen"),
    path(TRADITIONAL_PATH.lstrip("/"), traditional, name="traditional"),
    path(COMPARISON_PATH.lstrip("/"), comparison, name="comparison"),
    path(SERVICES_PATH.lstrip("/"), services, name="services"),
    path(SERVICE_COMPARISON_PATH.lstrip("/"), service_comparison, name="service_comparison"),
]
