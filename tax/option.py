"""Election timing for established businesses, including the exceptional first term."""
from datetime import date, timedelta

from tax.traditional import shift_month


def window(requested, rules):
    first, last = map(date.fromisoformat, rules["first_window"])
    if first <= requested <= last:
        return date(2027, 1, 1), tuple(map(date.fromisoformat, rules["first_cancel"]))
    if requested.year >= 2027 and requested.month in (3, 9):
        march = requested.month == 3
        start = date(requested.year + int(not march), 7 if march else 1, 1)
        cancel_end = date(requested.year, 5, 31) if march else date(requested.year, 11, 30)
        return start, (requested, cancel_end)
    return None, None


def election(data, period, rules):
    requested, cancelled = data["option_date"], data["cancel_date"]
    start, cancellation = window(requested, rules) if requested else (None, None)
    state = "Situação da opção desconhecida"
    active = None
    if data["option_status"] == "absent" and requested is None:
        active, state = False, "Sem opção vigente, conforme declaração"
    elif requested:
        if start is None:
            active, state = False, "Pedido fora da janela"
        elif cancelled and cancellation[0] <= cancelled <= cancellation[1]:
            active, state = False, "Opção cancelada no prazo"
        elif cancelled:
            state = "Cancelamento informado fora da janela. Conferir situação no Portal"
        elif period < start:
            active, state = False, "Opção com efeitos futuros"
        elif data["option_status"] == "active":
            active, state = True, "Opção vigente declarada, sem confirmação independente"
        elif data["option_status"] == "assumed":
            state = "Hipótese de opção tempestiva para o semestre, sem confirmação de vigência"
        else:
            state = "Pedido tempestivo sem confirmação de vigência"
    decision = data["decision_date"]
    next_start, next_cancel = window(decision, rules)
    refund = data["refund"]
    active_at_decision = bool(active and start <= decision)
    new_status = "Janela fechada para nova opção na data avaliada."
    if next_start:
        if active_at_decision:
            new_status = "Opção já vigente conforme declaração. A continuidade dispensa novo pedido."
        elif requested and requested <= decision and start == next_start and cancelled is None:
            new_status = "Já há pedido declarado para o semestre dessa janela."
        else:
            new_status = "Janela aberta, sujeita ao enquadramento e à situação da empresa no Portal."
    can_cancel = (cancellation[0] <= decision <= cancellation[1] and requested <= decision
                  and (cancelled is None or cancelled > decision)) if cancellation else None
    return dict(status=state, active=active, start=start,
                first_term_end=shift_month(start, 6) - timedelta(days=1) if start else None,
                cancellation_window=cancellation, new_option_start=next_start,
                new_cancellation_window=next_cancel,
                new_option_status=new_status,
                can_cancel_on_decision=can_cancel,
                return_start=next_start if active_at_decision and refund == "no" else None,
                return_status={"yes": "Retorno vedado por ressarcimento no ano corrente ou anterior.",
                               "no": "Renúncia sujeita à janela semestral e à situação no Portal.",
                               "unknown": "Retorno depende de confirmar ressarcimentos no ano corrente e anterior."}[refund],
                continuation="A escolha persiste nos semestres seguintes até renúncia válida.")
