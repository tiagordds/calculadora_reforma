"""Replay captured requests against archived binaries in an isolated working directory."""
import argparse
import json
from pathlib import Path
import shutil
import socket
import subprocess
import time
from datetime import datetime, timezone
from urllib.error import URLError

from probe import SCRATCH, digest, request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--java", default="java")
parser.add_argument("--output", type=Path, default=SCRATCH / "results/replay.json")
options = parser.parse_args()
lab = SCRATCH
out = lab.parent / "docs/evidencias/00a"
archive = lab / "preservado-00a"
java = options.java
results = []
for engine, database, jar, cases in (
    ("regular", "calculadora-pro.db", "api-regime-geral.jar", ["calculation", "single_2027"]),
    ("simples", "calculadora-pro.db", "api-simples-nacional.jar", ["calculation", "nfse_820001"]),
    ("simples", "compat58-pro.db", "api-simples-nacional.jar", ["calculation", "nfse_820001"]),
):
    captured = json.loads((out / (engine + ".json")).read_text(encoding="utf-8"))["cases"]
    working = lab / "replay" / engine / database.removesuffix(".db")
    db = working / "calculadora/db/calculadora-pro.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(archive / database, db)
    assert digest(db) == digest(archive / database)
    for port in (18200, 19200):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", port))
    args = ["-Xmx512m","-jar",str(archive / jar),"--spring.profiles.active=offline",
            "--server.address=127.0.0.1","--server.port=18200","--management.server.address=127.0.0.1",
            "--management.server.port=19200","--versao.url=http://127.0.0.1:1/unavailable",
            "--management.tracing.enabled=false"]
    with (working / "runtime.log").open("wb") as log:
        process = subprocess.Popen([java, *args], cwd=working, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline and process.poll() is None:
                try:
                    version = request(18200, captured["version"]["path"])
                    if version["status"] == 200:
                        break
                except (URLError, TimeoutError):
                    pass
                time.sleep(.1)
            else:
                raise RuntimeError("Replay did not start")
            for name in cases:
                ref = captured[name]
                got = request(18200, ref["path"], ref["input"])
                item = got["body"]["objetos"][0]
                matches = ref["body"] == got["body"]
                assert got["status"] == 200
                if database == "compat58-pro.db" and name == "nfse_820001":
                    assert item["estadoItem"] == "NAO_IMPLEMENTADO" and item["erros"][0]["code"] == "VSN-027"
                else:
                    assert matches
                results.append(dict(utc=datetime.now(timezone.utc).isoformat(), jar=jar, archive_db=database,
                                    reported_version=version["body"], input_from=engine+".json#cases."+name,
                                    http=got["status"], matches_v0059_body=matches, body=got["body"]))
        finally:
            process.terminate()
            process.wait(timeout=15)
options.output.parent.mkdir(parents=True, exist_ok=True)
options.output.write_text(json.dumps(results, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
print([(r["archive_db"],r["input_from"],r["matches_v0059_body"]) for r in results])
