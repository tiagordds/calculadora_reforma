"""Resolve one local, integrity-checked edition for the entire request."""
import hashlib
import json
import re
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ACTIVE = "sn-03-02"
DIGESTS = {
    "sn-03-01": "31802537494f45e1d84f8516fff8395a6c4e21e09b7d02fc9b5965ce1dc30bc5",
    "sn-03-02": "f96807afcc2d8899b74a13d62be7f52438672b1e0836ed9985cd452f9bb6f6d8",
}
ASSUMPTIONS_HASH = "efc644189b0120422b38192c75adf023317a8ff234a7d890de8dd2f643c76c62"
UNITS = dict(nominal="percent", shares="percent", deduction="BRL", bounds="BRL",
             annual_limit="BRL", annual_sublimit="BRL", excess_margin="percent")


class CatalogError(ValueError):
    pass


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError("Chave duplicada no catálogo.")
        result[key] = value
    return result


def read_pinned(path, digest):
    try:
        # Git may check text files out with CRLF on Windows.
        raw = path.read_bytes().replace(b"\r\n", b"\n")
    except OSError as exc:
        raise CatalogError("Arquivo da revisão indisponível.") from exc
    if hashlib.sha256(raw).hexdigest() != digest:
        raise CatalogError("Conteúdo divergente da revisão fixada.")
    return json.loads(raw, object_pairs_hook=unique_keys)


def number(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,12}(\.[0-9]{1,8})?", value):
        raise CatalogError("Valor decimal incompatível.")
    return Decimal(value)


def select_period(catalog, revision, when):
    if (catalog["id"] != "sn-traditional-retail" or catalog["revision"] != revision
            or catalog["regime"] != "Simples Nacional tradicional" or catalog["annex"] != "I"
            or catalog["territory"] != "BR-SC-4205407" or catalog["origin"] != "oficial"):
        raise CatalogError("Revisão ou perfil incompatível.")
    next_day = date(2027, 1, 1)
    selected = None
    for period in sorted(catalog["periods"], key=lambda row: row["start"]):
        start, end = date.fromisoformat(period["start"]), date.fromisoformat(period["end"])
        if start < next_day or end < start:
            raise CatalogError("Sobreposição ou intervalo inválido no catálogo.")
        if start > next_day:
            raise CatalogError("Lacuna de vigência no catálogo.")
        next_day = end + timedelta(days=1)
        if start <= when <= end:
            selected = period
    if next_day != date(2029, 1, 1) or selected is None:
        raise CatalogError("Sem vigência completa para a data solicitada.")
    if selected["units"] != UNITS:
        raise CatalogError("Unidade de parâmetro incompatível.")
    prior = selected["prior_year_limits"]
    if prior["year"] != 2026 or prior["territory"] != "BR-SC":
        raise CatalogError("Território ou vigência incompatível na triagem anual.")
    for record in (selected, prior):
        limit, sublimit, margin = (number(record[k]) for k in ("annual_limit", "annual_sublimit", "excess_margin"))
        if not 0 < sublimit < limit or not 0 < margin < 100:
            raise CatalogError("Limites anuais incompatíveis.")
    expected = [4] if revision == "sn-03-01" else [3, 4, 5]
    bands = selected["bands"]
    if [b["number"] for b in bands] != expected:
        raise CatalogError("Faixa ausente, duplicada ou incompatível.")
    previous = None
    for band in bands:
        low, high = number(band["above"]), number(band["through"])
        if low >= high or (previous is not None and low != previous):
            raise CatalogError("Fronteiras de faixa incompatíveis.")
        previous = high
        nominal = number(band["nominal"])
        if not 0 < nominal <= 100 or number(band["deduction"]) > low * nominal / 100:
            raise CatalogError("Nominal ou dedução incompatível.")
        if band["number"] == 4:
            shares = band["shares"]
            if (set(shares) != {"IRPJ", "CSLL", "CPP", "ICMS", "CBS", "IBS"}
                    or sum(map(number, shares.values())) != 100 or min(map(number, shares.values())) <= 0):
                raise CatalogError("Repartição ausente ou contraditória.")
    return selected


def resolve(revision, when):
    if revision not in DIGESTS:
        raise CatalogError("Revisão indisponível.")
    try:
        catalog = read_pinned(ROOT / "data" / (revision + ".json"), DIGESTS[revision])
        period = select_period(catalog, revision, when)
        assumptions = read_pinned(ROOT / "assumptions.json", ASSUMPTIONS_HASH)
        return catalog, period, assumptions
    except CatalogError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise CatalogError("Parâmetro obrigatório ausente ou inválido.") from exc
