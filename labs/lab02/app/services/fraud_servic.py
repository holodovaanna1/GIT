from app.domain.fraud import FraudCheckContext, FraudResult
from app.support.errors import DomainError
from app.support.types import risk_points

class FraudService:
    def __init__(self, rules=()):
        self._rules = tuple(rules)

    def check(self, context):
        amount_value = context.amount.amount
        currency = getattr(context.amount, "currency", None)

        if currency != "EUR":
            raise DomainError("CURRENCY_MISMATCH")
        if amount_value <= 0:
            raise DomainError("INVALID_CONTEXT")

        recent = context.recent_count
        if isinstance(recent, bool) or not isinstance(recent, int) or recent < 0:
            raise DomainError("INVALID_CONTEXT")

        score = 0
        codes = []

        if amount_value > 1000:
            score += 40
            codes.append("LARGE_AMOUNT")
        if context.merchant_category == "GAMBLING":
            score += 40
            codes.append("HIGH_RISK_MERCHANT")
        if recent >= 5:
            score += 20
            codes.append("MANY_RECENT_ATTEMPTS")

        if score < 0:
            score = 0
        elif score > 100:
            score = 100

        return FraudResult(score=score, triggered_rules=tuple(codes))

def make_entity(*args, **kwargs):
    return FraudCheckContext(*args, **kwargs)

def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)

def view(entity):
    return {
        'amount': entity.amount,
        'merchant_category': entity.merchant_category,
        'recent_count': entity.recent_count,
    }   

def new_service():
    return FraudService()
