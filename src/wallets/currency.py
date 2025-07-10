from dataclasses import dataclass


ALLOWED_CURRENCIES_CODES = set()


@dataclass(frozen=True, slots=True)
class Currency:
    code: str

    def __post_init__(self) -> None:
        if self.code not in ALLOWED_CURRENCIES_CODES:
            raise ValueError(f"Currency '{self.code}' is not allowed.")


def register_currency(code: str) -> Currency:
    if code in ALLOWED_CURRENCIES_CODES:
        raise ValueError(f"Currency '{code}' is already registered.")
    ALLOWED_CURRENCIES_CODES.add(code)
    return Currency(code)


rub = register_currency("RUB")
usd = register_currency("USD")
