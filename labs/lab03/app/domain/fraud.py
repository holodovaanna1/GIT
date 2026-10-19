from dataclasses import dataclass
from app.support.types import Money, positive, choice
from app.support.errors import DomainError


@dataclass(frozen=True)
class FraudCheckContext:
    amount: Money
    merchant_category: str
    recent_count: int = 0

    def __post_init__(self):
        positive(self.amount)
        if self.amount.currency != "EUR":
            raise DomainError("CURRENCY_MISMATCH")
        if type(self.recent_count) is not int or self.recent_count < 0:
            raise DomainError("INVALID_CONTEXT")
        choice(self.merchant_category, ("GROCERY", "RESTAURANT", "FUEL", "TRAVEL", "GAMBLING", "OTHER"), "INVALID_CATEGORY")


@dataclass(frozen=True)
class FraudResult:
    score: int
    triggered_rules: tuple

    def __post_init__(self):
        if type(self.score) is not int or not 0 <= self.score <= 100:
            raise DomainError("INVALID_RESULT")
        codes = tuple(self.triggered_rules)
        if any(not isinstance(code, str) or not code.strip() for code in codes) or len(codes) != len(set(codes)):
            raise DomainError("INVALID_RESULT")
        object.__setattr__(self, "triggered_rules", codes)

    @property
    def decision(self):
        return "DECLINE" if self.score >= 60 else "ALLOW"
