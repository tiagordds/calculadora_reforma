"""Replay two synthetic March 2027 items and check the monthly arithmetic."""
import argparse
from decimal import Decimal as D
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from urllib.error import URLError

LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[1]
sys.path.insert(0, str(ROOT / "scratch/00a"))
from probe import digest, request


def monthly():
    revenue = D("100000")
    history = 12 * revenue
    rate = (history * D(".107") - D("22500")) / history
    shares = dict(IRPJ="5.50", CSLL="3.50", CBS="15.33", CPP="42", ICMS="33.50", IBS=".17")
    amounts = {tax: revenue * rate * D(share) / 100 for tax, share in shares.items()}
    retained = rate * (1 - (D(shares["CBS"]) + D(shares["IBS"])) / 100)
    assert sum(amounts.values()) == rate * revenue == D("8825")
    assert retained == D(".07457125")
    assert sum(D(s) for s in shares.values()) == 100
    return dict(rate=str(rate), retained_rate=str(retained), monthly_das=str(rate*revenue),
                allocation={tax: str(value) for tax, value in amounts.items()})


def run_item(engine, java, working):
    archive = ROOT / "scratch/preservado-00a"
    source = ROOT / "docs/evidencias/00a" / (engine + ".json")
    cases = json.loads(source.read_text(encoding="utf-8"))["cases"]
    name = "single_2027" if engine == "regular" else "calculation"
    payload = cases[name]["input"]
    if engine == "regular":
        payload.update(dhFatoGerador="2027-03-15T10:00:00-03:00", municipio=4205407, uf="SC")
        payload["itens"] = [dict(numero=1, ncm="96081000", cst="000", cClassTrib="000001",
                                 baseCalculo="100.00", quantidade=1, unidade="UN",
                                 aliquotasNominais=dict(cbs="10.00", ibsEstadual="0.05", ibsMunicipal="0.05"))]
        jar = archive / "api-regime-geral.jar"
    else:
        payload["itens"][0].update(baseCalculo="100.00", valorImpostoSeletivo="0.00",
                                   pIBSSN="0.0150", pCBSSN="1.3529")
        jar = archive / "api-simples-nacional.jar"
    db = working / "calculadora/db/calculadora-pro.db"
    db.parent.mkdir(parents=True)
    shutil.copyfile(archive / db.name, db)
    inventory = json.loads((ROOT / "docs/evidencias/00a/inventario.json").read_text(encoding="utf-8"))
    jar_hash = digest(jar)["sha256"]
    db_hash = digest(db)["sha256"]
    assert jar_hash == inventory["archives"][jar.name]["sha256"]
    assert db_hash == inventory["archives"][db.name]["sha256"]
    for port in (18320,19320):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", port))
    args = [java, "-Xmx512m", "-jar", str(jar), "--spring.profiles.active=offline",
            "--server.address=127.0.0.1", "--server.port=18320", "--management.server.address=127.0.0.1",
            "--management.server.port=19320", "--versao.url=http://127.0.0.1:1/unavailable",
            "--management.tracing.enabled=false"]
    with (working / "runtime.log").open("wb") as log:
        process = subprocess.Popen(args, cwd=working, stdout=log, stderr=subprocess.STDOUT)
        try:
            limit = time.monotonic() + 90
            while process.poll() is None and time.monotonic() < limit:
                try:
                    version = request(18320, cases["version"]["path"])
                    if version["status"] == 200:
                        break
                except (URLError, TimeoutError):
                    pass
                time.sleep(.2)
            else:
                raise RuntimeError("Engine unavailable")
            path = cases[name]["path"]
            response = request(18320, path, payload)
            return dict(engine=engine, jar_sha256=jar_hash, db_sha256=db_hash,
                        commit=inventory["commits"][engine], version=version["body"],
                        method="POST", path=path, input=payload, http=response["status"], body=response["body"])
        finally:
            process.terminate()
            process.wait(timeout=20)


def sensitivity():
    # Only the hypothetical March case in CALCULATION_REFERENCE.md.
    price = D("100000")
    cbs_rate = D("0.10")
    ibs_rate = D("0.001")
    base = (price - D("2700")) / (1 + cbs_rate + ibs_rate)
    output_cbs = base * cbs_rate
    output_ibs = base * ibs_rate
    revenue = price - output_cbs - output_ibs
    retained_das = revenue * D(".07457125")
    cases = []
    for purchase_base in (D(0), D(15000), D(30000)):
        cbs_due = max(D(0), output_cbs - purchase_base * cbs_rate)
        ibs_due = max(D(0), output_ibs - purchase_base * ibs_rate)
        cases.append(dict(eligible_base=str(purchase_base), estimate=format(retained_das + cbs_due + ibs_due, ".2f")))
    assert [case["estimate"] for case in cases] == ["15717.31", "14202.31", "12687.31"]
    return dict(price=str(price), hypothetical_cbs_rate=str(cbs_rate), assumed_exclusions="2700",
                sales_base=str(base), revenue=str(revenue), retained_das=str(retained_das), cases=cases)


def check_responses(cases):
    regular, simples = cases
    assert all(case["http"] == 200 and len(case["body"]["objetos"]) == 1 for case in cases)
    item = regular["body"]["objetos"][0]
    assert item["estadoItem"] == "CALCULO_SIMULADO"
    taxes = item["tribCalc"]["IBSCBS"]["gIBSCBS"]
    assert D(taxes["gIBSUF"]["vIBSUF"]) == D(taxes["gIBSMun"]["vIBSMun"]) == D("0.05")
    assert D(taxes["gCBS"]["vCBS"]) == D("10.00")
    item = simples["body"]["objetos"][0]
    assert item["estadoItem"] == "CALCULADO"
    assert item["tribCalc"]["tpRBSN"] == 1
    assert D(item["tribCalc"]["vIBSSN"]) == D("0.02")
    assert D(item["tribCalc"]["vCBSSN"]) == D("1.35")
    assert D(simples["body"]["total"]["totalTributos"]) == D("1.37")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", default="java")
    parser.add_argument("--output", type=Path, default=LAB / "reference.json")
    options = parser.parse_args()
    result = dict(utc=datetime.now(timezone.utc).isoformat(), monthly=monthly(),
                  hypothetical_sensitivity=sensitivity(), cases=[])
    for name in ("regular", "simples"):
        with tempfile.TemporaryDirectory(dir=LAB) as temp_dir:
            result["cases"].append(run_item(name, options.java, Path(temp_dir)))
    options.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    check_responses(result["cases"])
    print(result["monthly"], [(case["engine"], case["http"]) for case in result["cases"]])
