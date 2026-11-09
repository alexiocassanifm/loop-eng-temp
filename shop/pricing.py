"""What a cart costs.

VAT applies to the items only. Shipping is a flat fee, added after VAT and never
taxed. Every rule about money that is not a tax lives here.
"""

from .cart import Cart
from .tax import vat


def total(cart: Cart) -> int:
    """Items, plus VAT on the items, plus shipping. In cents."""
    items = cart.subtotal()
    return items + vat(items) + cart.shipping
