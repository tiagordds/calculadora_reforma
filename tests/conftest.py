import json
from pathlib import Path

import pytest


EVIDENCE = Path(__file__).resolve().parents[1] / "docs/evidencias"


@pytest.fixture
def c03():
    return json.loads((EVIDENCE / "00b/reference.json").read_bytes())["cases"][0]


@pytest.fixture
def regular_cases():
    return json.loads((EVIDENCE / "00a/regular.json").read_bytes())["cases"]


def pytest_addoption(parser):
    parser.addoption("--record-engine", type=Path, help="Gravar somente as respostas sintéticas da prova real.")
