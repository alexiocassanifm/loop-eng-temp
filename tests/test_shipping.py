from shop.cart import Cart
from shop.pricing import shipping_for


def test_large_order_ships_free():
    assert shipping_for(Cart(shipping=590).add("a", 6000)) == 0


def test_small_order_pays_shipping():
    assert shipping_for(Cart(shipping=590).add("a", 4000)) == 590
