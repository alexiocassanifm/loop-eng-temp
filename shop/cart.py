from dataclasses import dataclass, field


@dataclass(frozen=True)
class Item:
    name: str
    unit_price: int  # cents
    qty: int = 1

    @property
    def line_total(self) -> int:
        return self.unit_price * self.qty


@dataclass
class Cart:
    items: list = field(default_factory=list)
    shipping: int = 0  # cents

    def add(self, name: str, unit_price: int, qty: int = 1) -> "Cart":
        if unit_price < 0 or qty < 1:
            raise ValueError(f"invalid item {name!r}: price {unit_price}, qty {qty}")
        self.items.append(Item(name, unit_price, qty))
        return self

    def subtotal(self) -> int:
        return sum(item.line_total for item in self.items)
