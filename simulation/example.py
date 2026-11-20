from decimal import Decimal


def pen_operation():
    """C03, capture 00B. Rates are percentage points, wire amounts are strings."""
    return {
        "id": "6194602ea71cbf9431c236de4409d920",
        "versao": "1.0.0",
        "dhFatoGerador": "2027-03-15T10:00:00-03:00",
        "municipio": 4205407,
        "uf": "SC",
        "itens": [{
            "numero": 1,
            "ncm": "96081000",
            "cst": "000",
            "cClassTrib": "000001",
            "baseCalculo": str(Decimal("100.00")),
            "quantidade": 1,
            "unidade": "UN",
            "aliquotasNominais": {
                "cbs": str(Decimal("10.00")),
                "ibsEstadual": str(Decimal("0.05")),
                "ibsMunicipal": str(Decimal("0.05")),
            },
        }],
    }
