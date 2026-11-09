"""What a cart costs.

VAT applies to the items only. Shipping is a flat fee, added after VAT and never
taxed. Every rule about money that is not a tax lives here.
"""

from .cart import Cart
from .tax import vat

FREE_SHIPPING_FROM = 5000  # cents


def shipping_for(cart: Cart) -> int:
    """Shipping is free for orders whose items come to 50.00 EUR or more."""
    return 0 if cart.subtotal() > FREE_SHIPPING_FROM else cart.shipping


def total(cart: Cart) -> int:
    """Items, plus VAT on the items, plus shipping. In cents."""
    items = cart.subtotal()
    return items + vat(items) + shipping_for(cart)
