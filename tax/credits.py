"""One acquisition group and one independent monthly account per tax."""
from decimal import Decimal

ZERO = Decimal(0)


class AccountError(ValueError):
    pass


def acquisition(data, tax, period):
    amount = data[tax + ("_transfer" if data["supplier"] == "simples" else "_credit")]
    result = dict(potential=data[tax+"_potential"], assessed=None, appropriated=None, reason="",
                  event_month=data["event_month"], acquisition_period=data["period"],
                  origin=data["credit_origin"], supplier=data["supplier"], rule=data["credit_rule"])
    if data["supplier"] == "exempt":
        result.update(potential=ZERO, assessed=ZERO, appropriated=ZERO,
                      reason="Operação desonerada declarada, sem crédito presumido (art. 49).")
    elif data["supplier"] == "unknown":
        result["potential"] = None
        result["reason"] = "Identifique o regime ou tratamento do fornecedor."
    elif data["credit_origin"] == "unknown" or not data["credit_evidence"] or amount is None:
        result["reason"] = "Informe o valor por tributo, o documento ou hipótese, a destinação e a regra de apropriação."
    else:
        result["assessed"] = amount
        event = data["event_month"]
        if data["credit_rule"] == "unknown":
            result["reason"] = "Confirme a extinção exigível, a exceção do art. 48 ou a apropriação declarada."
        elif event is None:
            result["reason"] = "Informe a competência em que todos os requisitos foram atendidos."
        else:
            result["appropriated"] = amount if event == period else ZERO
            result["reason"] = ("Apropriação do grupo no período declarado." if event == period else
                                "Evento em outra competência. O crédito deste grupo não entra neste mês.")
            if data["supplier"] == "simples":
                result["reason"] += " Limitado ao valor do Simples transferível conforme o documento (art. 47, § 9º)."
    return result


def account(debit, credit, opening, adjustment, reversal, extinguished, complete):
    available = used = net = closing = remaining = None
    if None not in (opening, adjustment, reversal, credit):
        available = opening + adjustment + credit - reversal
        if available < 0:
            raise AccountError("O estorno supera o crédito disponível do próprio tributo.")
    if debit is not None and extinguished is not None and extinguished > debit.quantize(Decimal("0.01")):
        raise AccountError("As extinções declaradas superam o débito do tributo.")
    if complete and None not in (available, debit):
        used = min(available, debit)
        net, closing = debit - used, available - used
        if extinguished is not None and extinguished <= net:
            remaining = net - extinguished
    return dict(debit=debit, opening=opening, adjustment=adjustment, reversal=reversal,
                appropriated=credit, available=available, used=used, net=net, closing=closing,
                extinguished=extinguished, remaining=remaining,
                reconciliation_required=net is not None and extinguished is not None and extinguished > net)


def customer(data):
    result = {}
    for seller in ("traditional", "hybrid"):
        result[seller] = {}
        for tax in ("cbs", "ibs"):
            potential = usable = None
            if data["buyer"] in ("consumer", "simples"):
                potential = usable = ZERO
            elif data["buyer"] == "regular" and data["buyer_document"]:
                potential = data[f"buyer_{seller}_{tax}"]
            result[seller][tax] = dict(potential=potential, usable=usable)
    return result
