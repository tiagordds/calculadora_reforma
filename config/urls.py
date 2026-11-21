from django.urls import path

from web.comparison_view import comparison
from web.middleware import COMPARISON_PATH, OPERATION_PATH, TRADITIONAL_PATH
from web.traditional_view import traditional
from web.views import home, pen


urlpatterns = [
    path("", home, name="home"),
    path(OPERATION_PATH.lstrip("/"), pen, name="pen"),
    path(TRADITIONAL_PATH.lstrip("/"), traditional, name="traditional"),
    path(COMPARISON_PATH.lstrip("/"), comparison, name="comparison"),
]
