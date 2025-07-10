from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import ValuesView


@dataclass
class Order:
    price: int


@dataclass
class DiscountManager:
    order: Order
    discounts_data: dict[int, "Discount"] = field(
        default_factory=dict, init=False
    )

    def show_discounts(self) -> ValuesView["Discount"]:
        return self.discounts_data.values()

    def apply_discounts(self, *discounts: "Discount") -> None:
        discount_values = self.show_discounts()
        for discount in discounts:
            if discount in discount_values:
                discount.apply(self.order)
                del self.discounts_data[discount.id]

    def add_discount(self, *discounts: "Discount") -> None:
        for discount in discounts:
            self.discounts_data[discount.id] = discount


class Discount(ABC):
    id: int
    discount_value: int

    def apply(self, order: Order) -> Order:
        new_price = self.count_discont(order.price)
        self.__class__.check_price(new_price)
        order.price = new_price
        return order

    @staticmethod
    def check_price(value: int) -> None:
        if value <= 0:
            raise ValueError("invalid value")

    @abstractmethod
    def count_discont(self, price: int) -> int:
        raise NotImplementedError


class FixedDiscount(Discount):

    def count_discont(self, price: int) -> int:
        return price - self.discount_value


class PercentDiscount(Discount):

    def count_discont(self, price: int) -> int:
        return price - (price * self.discount_value // 100)


class LoyaltyDiscount(Discount):
    loyalty_points: int

    def count_discont(self, price: int) -> int:
        return price - self.loyalty_points
