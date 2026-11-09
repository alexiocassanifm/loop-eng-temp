from .cart import Cart
from .receipt import render


def demo_cart() -> Cart:
    return Cart(shipping=590).add("Espresso beans 1kg", 2450).add("Filter papers", 390, qty=2)


if __name__ == "__main__":
    print(render(demo_cart()))
