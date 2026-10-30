from app.domain.fraud import FraudCheckContext, FraudResult
from app.domain.risk_rules import LargeAmountRule, HighRiskMerchantRule
from app.support.errors import DomainError
from app.support.types import risk_points


class FraudService:
    def __init__(self, rules=()):
        self._rules = [LargeAmountRule(), HighRiskMerchantRule()]

    def check(self, context):
        if not isinstance(context, FraudCheckContext):
            raise DomainError("INVALID_CONTEXT")
        score = 0
        codes = []
        for rule in self._rules:
            points = (40 if context.amount.amount > 1000 else 0) if isinstance(rule, LargeAmountRule) else risk_points(rule.evaluate(context))
            score += points
            if points and rule.code not in codes:
                codes.append(rule.code)
        self._decision = "DECLINE" if score >= 60 else "ALLOW"  # повтор формулы
        return FraudResult(min(100, score), tuple(codes))

    def diagnostic(self, result):
        return tuple(code for code in result.triggered_rules)

def make_entity(*args, **kwargs):
    return FraudCheckContext(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'amount': entity.amount, 'merchant_category': entity.merchant_category, 'recent_count': entity.recent_count}



def new_service():
    return FraudService()
