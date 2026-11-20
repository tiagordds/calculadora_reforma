import os
from pathlib import Path
import secrets
import subprocess
import sys

import pytest
from django.contrib.staticfiles import finders
from django.test import Client
from django.urls import reverse


ROOT = Path(__file__).resolve().parents[1]


def test_home(client):
    assert reverse("home") == "/"
    response = client.get("/")
    assert response.status_code == 200
    assert response["Content-Type"] == "text/html; charset=utf-8"
    assert response["X-Frame-Options"] == "DENY"
    assert response["X-Content-Type-Options"] == "nosniff"
    html = response.content.decode("utf-8")
    for fragment in (
        '<html lang="pt-BR">',
        "<title>Simulação tributária</title>",
        "<h1>Simulação tributária</h1>",
        'href="#calculadora">Conhecer a calculadora',
        'id="calculadora"',
        "Florianópolis",
        "revende",
        "Março de 2027",
        "Simples Nacional tradicional",
        "Apuração regular de IBS e CBS",
        "Os cálculos estarão disponíveis em etapas posteriores.",
    ):
        assert fragment in html


def test_home_stylesheet(client):
    assert 'href="/static/web/site.css"' in client.get("/").content.decode()
    assert Path(finders.find("web/site.css")) == ROOT / "web/static/web/site.css"


def test_head(client):
    response = client.head("/")
    assert response.status_code == 200
    assert response.content == b""


def test_post_requires_csrf_and_rejects_method(settings):
    client = Client(enforce_csrf_checks=True)
    assert client.post("/").status_code == 403
    token = secrets.token_hex(16)
    client.cookies[settings.CSRF_COOKIE_NAME] = token
    response = client.post("/", {"csrfmiddlewaretoken": token})
    assert response.status_code == 405
    assert response["Allow"] == "GET, HEAD"


def test_missing_route(client):
    assert client.get("/inexistente/").status_code == 404


@pytest.mark.parametrize("key", [None, ""])
def test_startup_requires_secret_key(key):
    env = os.environ.copy()
    env.pop("DJANGO_SECRET_KEY", None)
    if key is not None:
        env["DJANGO_SECRET_KEY"] = key
    result = subprocess.run(
        [sys.executable, "manage.py", "check"], cwd=ROOT, env=env, capture_output=True
    )
    assert result.returncode != 0
    assert b"ImproperlyConfigured" in result.stderr
    assert b"DJANGO_SECRET_KEY" in result.stderr


def test_default_settings_in_fresh_process():
    env = os.environ.copy()
    env.pop("DJANGO_DEBUG", None)
    env.pop("DJANGO_ALLOWED_HOSTS", None)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from config import settings as s; "
            "print(s.DEBUG, ','.join(s.ALLOWED_HOSTS), s.DATABASES['default']['NAME'])",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "False localhost,127.0.0.1 :memory:"
