from django.urls import path

from web.middleware import OPERATION_PATH
from web.views import home, pen


urlpatterns = [
    path("", home, name="home"),
    path(OPERATION_PATH.lstrip("/"), pen, name="pen"),
]
