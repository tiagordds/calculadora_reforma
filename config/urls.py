from django.urls import path

from web.middleware import OPERATION_PATH, TRADITIONAL_PATH
from web.traditional_view import traditional
from web.views import home, pen


urlpatterns = [
    path("", home, name="home"),
    path(OPERATION_PATH.lstrip("/"), pen, name="pen"),
    path(TRADITIONAL_PATH.lstrip("/"), traditional, name="traditional"),
]
