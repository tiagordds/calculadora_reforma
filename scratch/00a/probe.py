"""Local Phase 00A experiment. Run from the project root after packaging both JARs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import socket
import subprocess
from threading import Barrier
import time
from urllib.error import HTTPError, URLError
from urllib.request import build_opener, ProxyHandler, Request

SCRATCH = Path(__file__).resolve().parents[1]
OPEN_DATA = "/api/calculadora/dados-abertos"
REGULAR = "/api/calculadora/observabilidade/regime-geral"
SIMPLES = "/api/calculadora/observabilidade/simples-nacional"


def regular_cases():
    repo = SCRATCH / "regular"
    source = repo / "src/test/resources/entradas/calculoscorretos/Teste_000001_1.json"
    current = json.loads(source.read_text(encoding="utf-8"))
    example = (repo / "docs/exemplos.md").read_text(encoding="utf-8")
    mixed = json.loads(re.search(r"```json\s*(.*?)```", example, re.S).group(1))
    single = {**mixed, "itens": [{**mixed["itens"][2], "numero": 1}]}
    future = deepcopy(current)
    future["dhFatoGerador"] = future.pop("dataHoraEmissao").replace("2026", "2027")
    return [
        ("version", OPEN_DATA + "/versao", None),
        ("classification", OPEN_DATA + "/classificacoes-tributarias/cbs-ibs/class-trib/000001?data=2027-01-01", None),
        ("rate_2026", OPEN_DATA + "/aliquota-uf?codigoUf=43&data=2026-06-01", None),
        ("rate_2027", OPEN_DATA + "/aliquota-uf?codigoUf=43&data=2027-06-01", None),
        ("calculation", REGULAR, current),
        ("missing_rates_2027", REGULAR, future),
        ("single_2027", REGULAR, single),
        ("mixed_2027", REGULAR, mixed),
        ("strict_2027", "/api/calculadora/regime-geral", mixed),
        ("version_status", "/api/versao/status", None),
    ]


def simples_cases():
    # Values from SimplesNacionalControllerTest (case 2), including the supplied IS.
    item = dict(numero=1, cAtivSN="01", cClassTrib="000001", baseCalculo="950.00",
                valorImpostoSeletivo="50.00", pIBSSN="1.25", pCBSSN="2.75")
    example = dict(id="507f1f77bcf86cd799439011", versao="2.0.0", data="2027-03-15",
                   tpDoc="55", CRT="1", itens=[item])
    activity = "/api/calculadora/simples-nacional/atividades/01?data="
    return [
        ("version", "/api/versao", None),
        ("activity_2026", activity + "2026-03-15", None),
        ("activity_2027", activity + "2027-03-15", None),
        ("calculation", SIMPLES, example),
        ("previous_year", SIMPLES, {**example, "data": "2026-03-15"}),
        ("next_year", SIMPLES, {**example, "data": "2028-03-15"}),
        ("global_error", SIMPLES, {**example, "tpEnteGov": "7"}),
        ("missing_activity", SIMPLES, {**example, "itens": [{**item, "cAtivSN": "99"}]}),
        ("mixed", SIMPLES, {**example, "itens": [item, {**item, "numero": 2, "cClassTrib": "999999"}]}),
        ("missing_effective_rates", SIMPLES, {**example, "itens": [{**item, "pIBSSN": None, "pCBSSN": None}]}),
        ("nfse_820001", SIMPLES, {**example, "tpDoc": "91", "itens": [
            {**item, "cAtivSN": "07", "cClassTrib": "820001", "baseCalculo": "1000.00", "valorImpostoSeletivo": "0.00"}
        ]}),
        ("regular_option", SIMPLES, {**example, "tpRegimeIBSCBS": "1"}),
        ("version_status", "/api/versao/status", None),
    ]


def request(port, path, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = Request(f"http://127.0.0.1:{port}{path}", data=body,
                  headers={"Content-Type": "application/json", "Accept": "application/json"})
    client = build_opener(ProxyHandler({}))
    start = time.perf_counter()
    try:
        response = client.open(req, timeout=6)
    except HTTPError as error:
        response = error
    with response:
        raw = response.read()
        return dict(status=response.status, ms=round((time.perf_counter() - start) * 1000, 2),
                    app_version=response.headers.get("X-CALC-APP-VERSION"),
                    db_version=response.headers.get("X-CALC-DB-VERSION"),
                    warning=response.headers.get("x-warning-dados-simulados"),
                    body=json.loads(raw) if raw else None)


def parallel_trial(port, path, reference):
    # Establish a serial software reference for each distinct amount before releasing four workers.
    inputs = []
    expected = []
    for i in range(4):
        payload = deepcopy(reference)
        payload["itens"][0]["baseCalculo"] = str(500 + 100 * i)
        payload["id"] = f"rtc-00a-{i}"
        serial = request(port, path, payload)
        assert serial["status"] == 200 and serial["body"]["objetos"][0]["estadoItem"] == "CALCULADO"
        inputs.append(payload)
        expected.append(serial["body"])
    barrier = Barrier(4)

    def run(index):
        barrier.wait(timeout=10)
        result = request(port, path, inputs[index])
        return dict(id=inputs[index]["id"], base=inputs[index]["itens"][0]["baseCalculo"],
                    ms=result["ms"], status=result["status"],
                    matches_serial=result["body"] == expected[index])

    with ThreadPoolExecutor(max_workers=4) as pool:
        return list(pool.map(run, range(4)))


def process_sample(pid):
    if os.name == "nt":
        command = f"Get-Process -Id {pid} | Select-Object WorkingSet64,PeakWorkingSet64,CPU | ConvertTo-Json -Compress"
        return json.loads(subprocess.check_output(["powershell", "-NoProfile", "-Command", command]))
    return {"ps_rss_kib_cpu_time": subprocess.check_output(
        ["ps", "-o", "rss=,time=", "-p", str(pid)], text=True).strip()}


def digest(path):
    with path.open("rb") as file:
        return {"bytes": path.stat().st_size, "sha256": hashlib.file_digest(file, "sha256").hexdigest()}


def investigate(engine, java, output):
    regular = engine == "regular"
    jar_name = "api-regime-geral" if regular else "api-simples-nacional"
    port, management = (18080, 19101) if regular else (18082, 19103)
    for number in [port, management]:
        with socket.socket() as check:
            check.bind(("127.0.0.1", number))
    cases = regular_cases() if regular else simples_cases()
    directory = SCRATCH / engine
    jar = directory / "target" / (jar_name + ".jar")
    db = directory / "calculadora/db/calculadora-pro.db"
    args = ["-Xmx512m", "-jar", str(jar.relative_to(directory)), "--spring.profiles.active=offline",
            "--server.address=127.0.0.1", f"--server.port={port}", "--management.server.address=127.0.0.1",
            f"--management.server.port={management}", "--versao.url=http://127.0.0.1:1/unavailable",
            "--management.tracing.enabled=false"]
    report = dict(engine=engine, utc=datetime.now(timezone.utc).isoformat(), platform=platform.platform(),
                  cpu_logical=os.cpu_count(), jvm_args=args, jar=digest(jar), database=digest(db), cases={})
    with (SCRATCH / f"{engine}-runtime.log").open("wb") as log:
        start = time.perf_counter()
        proc = subprocess.Popen([java, *args], cwd=directory, stdout=log, stderr=subprocess.STDOUT)
        try:
            while True:
                if proc.poll() is not None or time.perf_counter() - start > 90:
                    raise RuntimeError(f"JVM unavailable, see {log.name}")
                try:
                    if request(port, cases[0][1])["status"] == 200:
                        break
                except (URLError, TimeoutError):
                    pass
                time.sleep(0.1)
            report["startup_to_version_s"] = round(time.perf_counter() - start, 3)
            report["after_start"] = process_sample(proc.pid)
            for name, path, payload in cases:
                result = request(port, path, payload)
                report["cases"][name] = dict(path=path, input=payload, **result)
                print(engine, name, result["status"], result["ms"], flush=True)
            case = report["cases"]["calculation"]
            report["warm_ms"] = []
            for _ in range(10):
                sample = request(port, case["path"], case["input"])
                assert sample["status"] == 200 and sample["body"] == case["body"]
                report["warm_ms"].append(sample["ms"])
            report["concurrent"] = parallel_trial(port, case["path"], case["input"])
            report["after_calls"] = process_sample(proc.pid)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
    output.mkdir(parents=True, exist_ok=True)
    (output / f"{engine}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", default="java")
    parser.add_argument("--engine", choices=("regular", "simples"))
    parser.add_argument("--output", type=Path, default=SCRATCH / "results")
    options = parser.parse_args()
    for name in ([options.engine] if options.engine else ("regular", "simples")):
        investigate(name, options.java, options.output)
