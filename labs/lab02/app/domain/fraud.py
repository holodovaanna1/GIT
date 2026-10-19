from decimal import Decimal
from app.support.types import Money, positive, choice
from app.support.errors import DomainError

class FraudCheckContext:

    def __init__(self, amount: Money, merchant_category: str, recent_count: int = 0):
        # ЛР2: положительная сумма
        positive(amount)

        # ЛР2: валюта должна быть EUR
        if amount.currency != "EUR":
            raise DomainError("CURRENCY_MISMATCH")

        # ЛР2: recent_count — целое >= 0, bool не считается целым
        if type(recent_count) is not int or recent_count < 0:
            raise DomainError("INVALID_CONTEXT")

        choice(merchant_category, ("GROCERY", "RESTAURANT", "FUEL", "TRAVEL", "GAMBLING", "OTHER"), "INVALID_CATEGORY")

        self.amount = amount
        self.merchant_category = merchant_category
        self.recent_count = recent_count


class FraudResult:
    def __init__(self, score: int, triggered_rules: tuple):
        # ЛР2: score — целое от 0 до 100
        if type(score) is not int or not 0 <= score <= 100:
            raise DomainError("INVALID_RESULT")

        codes = tuple(triggered_rules)
        if any(not isinstance(code, str) or not code.strip() for code in codes) or len(codes) != len(set(codes)):
            raise DomainError("INVALID_RESULT")

        self.score = score
        self.triggered_rules = codes


    @property
    def decision(self):
        return "DECLINE" if self.score >= 60 else "ALLOW"
    

    
