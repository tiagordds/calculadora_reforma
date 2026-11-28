from django.urls import path

from web.comparison_view import comparison
from web.middleware import COMPARISON_PATH, OPERATION_PATH, SERVICES_PATH, TRADITIONAL_PATH
from web.middleware import MIXED_COMPARISON_PATH, MIXED_PATH, SERVICE_COMPARISON_PATH
from web.mixed import mixed
from web.mixed_comparison import mixed_comparison
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
    path(MIXED_PATH.lstrip("/"), mixed, name="mixed"),
    path(MIXED_COMPARISON_PATH.lstrip("/"), mixed_comparison, name="mixed_comparison"),
    path(SERVICE_COMPARISON_PATH.lstrip("/"), service_comparison, name="service_comparison"),
]
