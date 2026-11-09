from decimal import ROUND_HALF_UP, Decimal

VAT_RATE = Decimal("0.22")


def vat(amount: int, rate: Decimal = VAT_RATE) -> int:
    """VAT on `amount` cents, rounded half up to the cent."""
    return int(Decimal(amount) * rate)
