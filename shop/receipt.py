from .cart import Cart
from .pricing import total
from .tax import vat


def money(cents: int) -> str:
    return f"{cents / 100} EUR"


def render(cart: Cart) -> str:
    lines = [f"{item.qty} x {item.name:<20} {money(item.line_total)}" for item in cart.items]
    items = cart.subtotal()
    lines += [
        f"{'items':<24} {money(items)}",
        f"{'VAT':<24} {money(vat(items))}",
        f"{'shipping':<24} {money(cart.shipping)}",
        f"{'TOTAL':<24} {money(total(cart))}",
    ]
    return "\n".join(lines)
