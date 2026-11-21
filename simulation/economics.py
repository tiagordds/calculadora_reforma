"""Compare obligations only for matching sales, periods and settlement stages."""


def differences(traditional, hybrid, traditional_basis, hybrid_basis):
    if traditional_basis != hybrid_basis or traditional is None or hybrid is None:
        return None
    price = traditional_basis["final_price"]
    delta = hybrid - traditional
    return dict(amount=delta, percent=delta*100/traditional if traditional else None,
                traditional_burden=traditional*100/price if price else None,
                hybrid_burden=hybrid*100/price if price else None)
