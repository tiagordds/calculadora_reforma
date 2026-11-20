"""Interpret the regular observable contract for the supported 2027 cases."""
from dataclasses import dataclass
from decimal import Decimal
import re

from .manifest import EngineError


@dataclass(frozen=True)
class Amounts:
    base: Decimal
    cbs: Decimal
    state_ibs: Decimal
    city_ibs: Decimal
    ibs: Decimal

    @property
    def combined(self):
        return self.cbs + self.ibs


@dataclass(frozen=True)
class Item:
    number: int
    state: str
    amounts: Amounts | None
    memory: tuple
    errors: tuple


@dataclass(frozen=True)
class OperationResult:
    items: tuple[Item, ...]
    totals: Amounts | None
    completeness: str


def require(condition):
    if not condition:
        raise EngineError("contract")


def money(value):
    require(isinstance(value, str) and re.fullmatch(r"[0-9]{1,16}\.[0-9]{2}", value))
    return Decimal(value)


def read_item(row, source, index):
    number, state = row["nObj"], row["estadoItem"]
    if state == "INCONSISTENCIA_ENTRADA":
        errors = row["erros"]
        require(isinstance(errors, list) and errors and "tribCalc" not in row)
        for error in errors:
            require(all(isinstance(error[k], str) and error[k] for k in ("code", "pointer", "title")))
            require(re.fullmatch(r"REG-[0-9]{3}", error["code"]))
            require(re.fullmatch(rf"#/itens/{index}(?:/[A-Za-z0-9_]+)*", error["pointer"]))
        return Item(number, state, None, (), tuple(errors))
    require(state == "CALCULO_SIMULADO" and "erros" not in row)
    tax = row["tribCalc"]["IBSCBS"]
    require(tax["CST"] == source["cst"] and tax["cClassTrib"] == source["cClassTrib"])
    group = tax["gIBSCBS"]
    if "baseCalculo" in source and "impostoSeletivo" not in source:
        require(money(group["vBC"]) == Decimal(str(source["baseCalculo"])))
    cbs, uf, city = group["gCBS"], group["gIBSUF"], group["gIBSMun"]
    amounts = Amounts(money(group["vBC"]), money(cbs["vCBS"]), money(uf["vIBSUF"]),
                      money(city["vIBSMun"]), money(group["vIBS"]))
    require(amounts.ibs == amounts.state_ibs + amounts.city_ibs)
    memory = []
    for label, data, rate_key, source_key in (
        ("CBS", cbs, "pCBS", "cbs"), ("IBS estadual", uf, "pIBSUF", "ibsEstadual"),
        ("IBS municipal", city, "pIBSMun", "ibsMunicipal"),
    ):
        rate = data[rate_key]
        require(isinstance(rate, str) and re.fullmatch(r"[0-9]{1,3}(\.[0-9]{1,8})?", rate))
        require(Decimal(rate) == Decimal(str(source["aliquotasNominais"][source_key])))
        require(isinstance(data["memoriaCalculo"], str) and data["memoriaCalculo"].strip())
        memory.append((label, data["memoriaCalculo"]))
    return Item(number, state, amounts, tuple(memory), ())


def interpret(payload, reply):
    try:
        objects = reply["body"]["objetos"]
        sources = {item["numero"]: (item, index) for index, item in enumerate(payload["itens"])}
        require(len(sources) == len(payload["itens"]) and 0 < len(sources) <= 10)
        require(isinstance(objects, list) and len(objects) == len(sources))
        seen = set()
        items = []
        for row in objects:
            number = row["nObj"]
            require(type(number) is int and number in sources and number not in seen)
            seen.add(number)
            source, index = sources[number]
            items.append(read_item(row, source, index))
        known = [item.amounts for item in items if item.amounts is not None]
        if not known:
            require("total" not in reply["body"])
            return OperationResult(tuple(items), None, "Não calculado")
        require(reply["headers"].get("x-warning-dados-simulados") == "6")
        total = reply["body"]["total"]["tribCalc"]["IBSCBSTot"]
        ibs = total["gIBS"]
        amounts = Amounts(money(total["vBCIBSCBS"]), money(total["gCBS"]["vCBS"]),
                          money(ibs["gIBSUF"]["vIBSUF"]), money(ibs["gIBSMun"]["vIBSMun"]),
                          money(ibs["vIBS"]))
        # Reconcile the engine's item amounts and totals, without redoing its tax rules.
        for field in ("base", "cbs", "state_ibs", "city_ibs", "ibs"):
            require(getattr(amounts, field) == sum(getattr(item, field) for item in known))
        completeness = "Completo no recorte" if len(known) == len(items) else "Parcial"
        return OperationResult(tuple(items), amounts, completeness)
    except (KeyError, IndexError, TypeError) as exc:
        raise EngineError("contract") from exc
