from decimal import Decimal
from app.support.types import Money, positive, choice
from app.support.errors import DomainError


# ЛР1: FraudCheckContext вместо словаря.
class FraudCheckContext:

    def __init__(self, amount: Money, currency: str, category: str):
        positive(amount)
        if not currency or not currency.strip():
            raise DomainError("INVALID_CONTEXT")
        if not category or not category.strip():
            raise DomainError("INVALID_CONTEXT")

        self.amount = amount
        self.currency = currency
        self.category = category


class FraudResult:

    def __init__(self, score: int, triggered_rules: tuple):
        if type(score) is not int or not 0 <= score <= 100:
            raise DomainError("INVALID_RESULT")

        codes = tuple(triggered_rules)
        if any(not isinstance(code, str) or not code.strip() for code in codes):
            raise DomainError("INVALID_RESULT")

        self.score = score
        self.triggered_rules = codes

    @property
    def decision(self):
        return "DECLINE" if self.score >= 60 else "ALLOW"
