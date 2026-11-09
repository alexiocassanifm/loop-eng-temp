import pytest

from shop.cart import Cart


def test_subtotal_sums_lines():
    cart = Cart().add("a", 1000).add("b", 250, qty=3)
    assert cart.subtotal() == 1750


def test_rejects_negative_price():
    with pytest.raises(ValueError):
        Cart().add("a", -1)


def test_rejects_zero_quantity():
    with pytest.raises(ValueError):
        Cart().add("a", 100, qty=0)
