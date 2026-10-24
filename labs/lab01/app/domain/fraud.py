from decimal import Decimal
from app.support.types import Money, positive, choice
from app.support.errors import DomainError

class FraudCheckContext:
    def __init__(self, amount: Money, currency: str = "EUR",\
                 category: str = "UNKNOWN", recent_count: int = 0):
        positive(amount)
        if not currency or not currency.strip():
            raise DomainError("INVALID_CONTEXT")
        if not category or not category.strip():
            raise DomainError("INVALID_CONTEXT")
        if type(recent_count) is not int or recent_count < 0:
            raise DomainError("INVALID_CONTEXT")

        self.amount = amount
        self.currency = currency
        self.category = category
        self.recent_count = recent_count

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
