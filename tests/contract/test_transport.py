from io import BytesIO
from unittest.mock import Mock

import pytest
import requests

from adapters import manifest, transport
from adapters.manifest import EngineError


def response(data=b'{"ok":true}', status=200, **headers):
    reply = requests.Response()
    reply.status_code = status
    reply.headers.update({"Content-Type": "application/json", **headers})
    reply.raw = BytesIO(data)
    return reply


@pytest.mark.parametrize("status,code", [(302, "contract"), (400, "rejected"), (404, "missing"),
                                         (422, "rejected"), (504, "timeout"), (503, "unavailable")])
def test_http_status(status, code):
    session = Mock()
    session.request.return_value = response(status=status)
    with pytest.raises(EngineError) as error:
        transport.read_json(session, manifest.CALC_PATH, {})
    assert error.value.code == code
    session.request.assert_called_once_with("POST", manifest.ORIGIN + manifest.CALC_PATH, json={},
                                            timeout=(0.5, 2), allow_redirects=False, stream=True)


@pytest.mark.parametrize("data,headers", [
    (b'{}', {"Content-Type": "text/html"}), (b'{}', {"Content-Length": "1048577"}),
    (b' ' * 1048577, {}), (b'{"a":1,"a":2}', {}), (b'[]', {}),
    (b'{"a":NaN}', {}), (b'???', {}), (b'{}', {"Content-Encoding": "gzip"}),
])
def test_invalid_body(data, headers):
    session = Mock()
    session.request.return_value = response(data, **headers)
    with pytest.raises((ValueError, EngineError)):
        transport.read_json(session, manifest.CALC_PATH)


@pytest.mark.parametrize("mismatch", ["versaoApp", "versaoDb", "ambiente", "post_header"])
def test_version_and_server_destination(monkeypatch, tmp_path, mismatch):
    session = requests.Session()
    monkeypatch.setattr(transport, "EngineSession", lambda: session)
    version = {"versaoApp": "1.6.1", "versaoDb": "V0059", "ambiente": "offline"}
    if mismatch != "post_header":
        version[mismatch] = "unexpected"
    read = Mock(side_effect=[{"body": version}, {"headers": {"x-calc-app-version": "1.6.1"}}])
    monkeypatch.setattr(transport, "read_json", read)
    with pytest.raises(EngineError) as error:
        transport.exchange({"itens": []}, tmp_path)
    assert error.value.code == "version"
    assert read.call_count == (2 if mismatch == "post_header" else 1)
    assert not session.trust_env
    assert session.adapters["https://"].max_retries.total == 0


def test_altered_or_absent_artifact(monkeypatch, tmp_path):
    jar = tmp_path / "synthetic.jar"
    monkeypatch.setattr(manifest, "JAR", jar)
    with pytest.raises(EngineError, match="indisponível"):
        manifest.verify_artifacts()
    jar.write_bytes(b"unqualified")
    with pytest.raises(EngineError, match="diverge"):
        manifest.verify_artifacts()
