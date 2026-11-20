"""Bounded HTTP transport. Invoked in a disposable Python process by regular.call."""
import json
from pathlib import Path
import sys

import requests
from urllib3.exceptions import ReadTimeoutError

from .manifest import (
    APP, CALC_PATH, DATABASE, EngineError, ORIGIN, READY, RUNTIME, VERSION_PATH,
    verify_artifacts,
)

MAX_BYTES = 1024 * 1024
VERSION_HEADERS = ("x-calc-app-version", "x-calc-db-version", "x-warning-dados-simulados")


class EngineSession(requests.Session):
    def get_redirect_target(self, response):
        # Session.send otherwise consumes a redirect body to prepare Response.next.
        return None


def unique_object(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("duplicate JSON field")
    return result


def read_json(session, path, payload=None):
    method = "GET" if payload is None else "POST"
    with session.request(method, ORIGIN + path, json=payload, timeout=(0.5, 2),
                         allow_redirects=False, stream=True) as response:
        status = response.status_code
        if status in (400, 422):
            raise EngineError("rejected")
        if status == 404:
            raise EngineError("missing")
        if status in (408, 504):
            raise EngineError("timeout")
        if status == 429 or status >= 500:
            raise EngineError("unavailable")
        if status != 200:
            raise EngineError("contract")
        if response.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            raise EngineError("contract")
        if response.headers.get("Content-Encoding", "identity") != "identity":
            raise EngineError("contract")
        size = response.headers.get("Content-Length")
        if size is not None and (not size.isdecimal() or int(size) > MAX_BYTES):
            raise EngineError("contract")
        raw = bytearray()
        for block in response.iter_content(16384):
            raw.extend(block)
            if len(raw) > MAX_BYTES:
                raise EngineError("contract")
        body = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=invalid_number)
        if not isinstance(body, dict):
            raise EngineError("contract")
        headers = {name: response.headers[name] for name in VERSION_HEADERS if name in response.headers}
        return {"http": status, "headers": headers, "body": body}


def invalid_number(value):
    raise ValueError("non-finite JSON number")


def exchange(payload, credentials):
    with EngineSession() as session:
        session.trust_env = False
        session.headers["Accept-Encoding"] = "identity"
        session.verify = str(credentials / "ca.pem")
        session.cert = (str(credentials / "client.pem"), str(credentials / "client.key"))
        version = read_json(session, VERSION_PATH)["body"]
        if (version.get("versaoApp"), version.get("versaoDb"), version.get("ambiente")) != (
            APP, DATABASE, "offline"
        ):
            raise EngineError("version")
        if payload is None:
            return version
        reply = read_json(session, CALC_PATH, payload)
        headers = reply["headers"]
        if (headers.get(VERSION_HEADERS[0]), headers.get(VERSION_HEADERS[1])) != (APP, DATABASE):
            raise EngineError("version")
        return {**reply, "version": version}


def main():
    command = json.load(sys.stdin)
    try:
        verify_artifacts()
        # Bootstrap passes its fresh identity before publishing the readiness marker.
        name = command.get("instance") or READY.read_text(encoding="ascii")
        if not name.startswith("instance-") or Path(name).name != name:
            raise EngineError("unavailable")
        result = exchange(command["payload"], RUNTIME / name)
    except EngineError as exc:
        result = {"error": exc.code}
    except requests.Timeout:
        result = {"error": "timeout"}
    except requests.ConnectionError as exc:
        reason = exc.args[0] if exc.args else None
        result = {"error": "timeout" if isinstance(reason, ReadTimeoutError) else "unavailable"}
    except (requests.exceptions.ChunkedEncodingError, ValueError, RecursionError):
        result = {"error": "contract"}
    except (OSError, requests.RequestException):
        result = {"error": "unavailable"}
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
