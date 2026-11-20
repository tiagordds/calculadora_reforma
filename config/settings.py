import os

from django.core.exceptions import ImproperlyConfigured


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY.strip():
    raise ImproperlyConfigured("Defina DJANGO_SECRET_KEY no ambiente.")

debug_value = os.environ.get("DJANGO_DEBUG", "0")
if debug_value not in {"0", "1"}:
    raise ImproperlyConfigured("DJANGO_DEBUG aceita apenas 0 ou 1.")
DEBUG = debug_value == "1"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
INSTALLED_APPS = ["web", "django.contrib.staticfiles"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "web.middleware.private_operation",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True},
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True
STATIC_URL = "/static/"
CSRF_COOKIE_AGE = None
DATA_UPLOAD_MAX_MEMORY_SIZE = 65536
CSRF_FAILURE_VIEW = "web.views.csrf_failure"
# Local access logs can include an arbitrary query string on rejected requests.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"discard": {"class": "logging.NullHandler"}},
    "loggers": {
        name: {"handlers": ["discard"], "propagate": False}
        for name in ("django.server", "django.request", "django.security")
    },
}
