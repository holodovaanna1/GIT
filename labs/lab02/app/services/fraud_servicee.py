from app.domain.fraud import FraudCheckContext, FraudResult
from app.support.errors import DomainError
from app.support.types import risk_points


class FraudService:
    def __init__(self, rules=()):
        self._rules = tuple(rules)

    def check(self, context):
        if not isinstance(context, FraudCheckContext):
            raise DomainError("INVALID_CONTEXT")
        score, codes = 0, []
        if context.amount.amount > 1000:
            score += 40
            codes.append("LARGE_AMOUNT")
        if context.merchant_category == "GAMBLING":
            score += 40
            codes.append("HIGH_RISK_MERCHANT")
        return FraudResult(score, tuple(codes))

def make_entity(*args, **kwargs):
    return FraudCheckContext(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'amount': entity.amount, 'merchant_category': entity.merchant_category, 'recent_count': entity.recent_count}



def new_service():
    return FraudService()
