from shop.cart import Cart
from shop.pricing import total


def test_total_is_items_plus_vat_plus_shipping():
    cart = Cart(shipping=500).add("a", 4000)
    assert total(cart) == 4000 + 880 + 500


def test_shipping_is_not_taxed():
    assert total(Cart(shipping=700)) == 700
