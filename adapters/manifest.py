import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scratch/regular"
RUNTIME = ROOT / "scratch/phase02"
READY = RUNTIME / "ready"
APP = "1.6.1"
DATABASE = "V0059"
COMMIT = "150cccbe414d4a5edea703e4f7a424af5aa222c7"
JAR = ENGINE / "target/api-regime-geral.jar"
DB = ENGINE / "calculadora/db/calculadora-pro.db"
JAR_HASH = "3f7baa20442301e2ba6733fc274263a8756a7e21b3ed4e4020b0f1ecf51f9d61"
DB_HASH = "4160a29e4f1a6a2c4f2d5d5527b64af2a84fb4ea2915693b70104865db533293"
ORIGIN = os.environ.get("REGULAR_ENGINE_URL", "https://127.0.0.1:18080")
if ORIGIN not in {"https://127.0.0.1:18080", "https://regular:8080"}:
    raise ValueError("Destino interno do motor fora da lista permitida.")
VERSION_PATH = "/api/calculadora/dados-abertos/versao"
CALC_PATH = "/api/calculadora/observabilidade/regime-geral"


class EngineError(Exception):
    MESSAGES = {
        "unavailable": "Motor indisponível. Tente calcular novamente quando o serviço estiver pronto.",
        "timeout": "O motor excedeu o prazo de resposta. Tente calcular novamente.",
        "busy": "O motor está ocupado. Aguarde um instante e tente novamente.",
        "version": "A edição do motor ou da base diverge da combinação autorizada.",
        "contract": "O motor devolveu uma resposta incompatível com o contrato da operação.",
        "rejected": "O motor rejeitou a entrada deste exemplo.",
        "missing": "A referência necessária ao cálculo está indisponível.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.MESSAGES[code])


def verify_artifacts():
    for path, expected in ((JAR, JAR_HASH), (DB, DB_HASH)):
        try:
            with path.open("rb") as stream:
                actual = hashlib.file_digest(stream, "sha256").hexdigest()
        except OSError as exc:
            raise EngineError("unavailable") from exc
        if actual != expected:
            raise EngineError("version")
