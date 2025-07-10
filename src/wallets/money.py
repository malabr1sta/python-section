from dataclasses import dataclass, field, InitVar
from decimal import Decimal
from functools import wraps
from typing import Callable, KeysView, Self

from wallets import (
    currency as wallets_curr,
    exceptions as wallets_except,
)


def check_currency(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, other):
        if self.currency != other.currency:
            raise wallets_except.NotComparisonException(self, other)
        return method(self, other)
    return wrapper


@dataclass(slots=True, frozen=True, kw_only=True)
class Money:
    currency: wallets_curr.Currency
    value: Decimal = Decimal("0.0")

    def __post_init__(self) -> None:
        if self.value < Decimal("0.0"):
            raise wallets_except.NegativeValueException("value < 0 invalid")

    @check_currency
    def __add__(self, other) -> "Money":
        new_value = self.value + other.value
        return self.__class__(value=new_value, currency=self.currency)

    @check_currency
    def __sub__(self, other) -> "Money":
        new_value = self.value - other.value
        return self.__class__(value=new_value, currency=self.currency)


class Wallet:
    __slots__ = ("__holdings",)
    __holdings: dict[wallets_curr.Currency, Money]

    def __init__(self, *args: Money) -> None:
        self.__holdings = {}
        self.add(*args)

    @property
    def currencies(self) -> KeysView[wallets_curr.Currency]:
        return self.__holdings.keys()

    def __contains__(self, item: wallets_curr.Currency) -> bool:
        return item in self.currencies

    def __len__(self) -> int:
        return len(self.__holdings)

    def __setitem__(self, key: wallets_curr.Currency, value: Money) -> Self:
        if key in self:
            raise ValueError(f"{key.code} already exists")
        self.__holdings[key] = value
        return self

    def __getitem__(self, key: wallets_curr.Currency) -> Money | None:
        if key not in self:
            raise KeyError(f"{key} not in wallet")
        return self.__holdings.get(key, None)

    def __delitem__(self, key: wallets_curr.Currency) -> None:
        if key not in self:
            raise KeyError(key)
        del self.__holdings[key]

    def add(self, *args: Money) -> Self:
        for money in args:
            if self.__holdings.get(money.currency, None) is None:
                self.__holdings[money.currency] = money
                continue
            self.__holdings[money.currency] += money
        return self

    def sub(self, *args: Money) -> Self:
        for money in args:
            if self.__holdings.get(money.currency, None) is None:
                raise KeyError(money.currency)
            self.__holdings[money.currency] -= money
        return self
