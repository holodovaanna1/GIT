from dataclasses import dataclass
from decimal import Decimal
from app.support.types import Money, positive, choice
from app.support.errors import DomainError


# ЛР1: FraudCheckContext вместо словаря.
@dataclass(frozen=True)
class FraudCheckContext:
    amount: Money
    currency: str
    category: str

    def __post_init__(self):
        positive(self.amount)
        if not self.currency or not self.currency.strip():
            raise DomainError("INVALID_CONTEXT")
        if not self.category or not self.category.strip():
            raise DomainError("INVALID_CONTEXT")

    def describe(self) -> str:
        """Бонусное задание: возвращает строку вида '100.00 EUR:RESTAURANT:0'."""
        return f"{self.amount.amount:.2f} {self.currency}:{self.category}:0"


@dataclass(frozen=True)
class FraudResult:
    score: int
    triggered_rules: tuple

    def __post_init__(self):
        if type(self.score) is not int or not 0 <= self.score <= 100:
            raise DomainError("INVALID_RESULT")
        codes = tuple(self.triggered_rules)
        if any(not isinstance(code, str) or not code.strip() for code in codes):
            raise DomainError("INVALID_RESULT")
        object.__setattr__(self, "triggered_rules", codes)

    @property
    def decision(self):
        return "DECLINE" if self.score >= 60 else "ALLOW"
