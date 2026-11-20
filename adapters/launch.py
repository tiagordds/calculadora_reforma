"""Start one pinned Java engine. Publish its private client identity after C03 passes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from time import monotonic, sleep

from simulation.example import pen_operation
from .manifest import ENGINE, EngineError, JAR, ORIGIN, READY, RUNTIME, verify_artifacts
from .regular import call

# SHA-256 of canonical UTF-8 cases[0].body from the independent 00B capture.
CANARY_HASH = "b5e0023c01fe1a247192423f850e2569ea6e379d0f9d9460429b8a516d4dc710"


def create_identity(directory, openssl):
    def run(*args):
        subprocess.run([openssl, *args], cwd=directory, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    run("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "30",
        "-subj", "/CN=Regular Local CA", "-keyout", "ca.key", "-out", "ca.pem",
        "-addext", "basicConstraints=critical,CA:TRUE", "-addext", "keyUsage=critical,keyCertSign,cRLSign")
    for name, usage in (("server", "serverAuth"), ("client", "clientAuth")):
        run("req", "-new", "-newkey", "rsa:2048", "-nodes", "-subj", f"/CN={name}",
            "-keyout", name + ".key", "-out", name + ".csr")
        extensions = ("basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\n"
                      f"extendedKeyUsage={usage}\nsubjectKeyIdentifier=hash\nauthorityKeyIdentifier=keyid\n")
        if name == "server":
            extensions += "subjectAltName=IP:127.0.0.1,DNS:regular\n"
        (directory / "extensions").write_text(extensions, encoding="ascii")
        run("x509", "-req", "-in", name + ".csr", "-CA", "ca.pem", "-CAkey", "ca.key",
            "-CAcreateserial", "-days", "30", "-extfile", "extensions", "-out", name + ".pem")
    (directory / "ca.key").unlink()


def qualify(java, directory):
    limit = monotonic() + 90
    while java.poll() is None and monotonic() < limit:
        try:
            call(None, instance=directory.name)
            break
        except EngineError as exc:
            if exc.code not in ("unavailable", "timeout"):
                raise
            sleep(0.4)
    else:
        raise SystemExit("Inicialização do motor falhou ou excedeu 90 segundos.")
    reply = call(pen_operation(), instance=directory.name)
    canonical = json.dumps(reply["body"], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    if (hashlib.sha256(canonical.encode()).hexdigest() != CANARY_HASH
            or reply["headers"].get("x-warning-dados-simulados") != "6"):
        raise SystemExit("O canário divergiu da captura qualificada.")
    marker = directory / "ready"
    marker.write_text(directory.name, encoding="ascii")
    marker.replace(READY)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", default=shutil.which("java"))
    parser.add_argument("--openssl", default=shutil.which("openssl"))
    args = parser.parse_args()
    if not args.java or not args.openssl:
        parser.error("Indique Java 21 e OpenSSL 3 por caminho ou PATH.")
    java_exe = str(Path(args.java).resolve())
    version = subprocess.check_output([java_exe, "-version"], stderr=subprocess.STDOUT)
    if not re.search(rb'version "21[."]', version):
        parser.error("A revisão qualificada requer Java 21.")
    verify_artifacts()
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=RUNTIME, prefix="instance-") as tmp, TemporaryDirectory() as private:
        directory = Path(tmp)
        server = Path(private)
        create_identity(server, str(Path(args.openssl).resolve()))
        for name in ("ca.pem", "client.pem", "client.key"):
            shutil.copy2(server / name, directory / name)
        container = ORIGIN == "https://regular:8080"
        java_args = [
            java_exe, "-Xmx512m", "-jar", str(JAR), "--spring.profiles.active=offline",
            "--server.address=" + ("0.0.0.0" if container else "127.0.0.1"),
            "--server.port=" + ("8080" if container else "18080"), "--management.server.port=-1",
            "--versao.url=http://127.0.0.1:1/unavailable", "--management.tracing.enabled=false",
            "--logging.level.root=OFF", "--logging.level.br.gov.serpro.rtc=OFF",
            "--server.ssl.enabled=true", "--server.ssl.client-auth=need",
            "--server.ssl.certificate=" + (server / "server.pem").as_uri(),
            "--server.ssl.certificate-private-key=" + (server / "server.key").as_uri(),
            "--server.ssl.trust-certificate=" + (directory / "ca.pem").as_uri(),
        ]
        with subprocess.Popen(java_args, cwd=ENGINE, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL) as java:
            try:
                qualify(java, directory)
                print(f"Motor pronto. JVM {java.pid}. Canário C03 conferido.", flush=True)
                java.wait()
            except KeyboardInterrupt:
                pass
            finally:
                java.terminate()
                java.wait()
                if READY.exists() and READY.read_text(encoding="ascii") == directory.name:
                    READY.unlink()


if __name__ == "__main__":
    main()
