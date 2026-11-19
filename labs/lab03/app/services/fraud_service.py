from app.domain.fraud import FraudCheckContext, FraudResult
from app.domain.risk_rules import (LargeAmountRule, HighRiskMerchantRule, ManyRecentAttemptsRule)
from app.support.errors import DomainError
from app.support.types import risk_points


class FraudService:
    def __init__(self, rules=None):
        if rules is None:
            self._rules = (LargeAmountRule(), HighRiskMerchantRule(), ManyRecentAttemptsRule())
        else:
            self._rules = tuple(rules)

    def check(self, context):
        if not isinstance(context, FraudCheckContext):
            raise DomainError("INVALID_CONTEXT")

        total = 0
        codes = []

        for rule in self._rules:
            points = rule.evaluate(context)
            
            if type(points) is not int or points < 0 or points > 100:
                raise DomainError("INVALID_RULE_RESULT")

            if points > 0:
                total += risk_points(points)

                if rule.code not in codes:
                    codes.append(rule.code)

        final_score = min(total, 100)

        return FraudResult(
            score=final_score,
            triggered_rules=tuple(codes)
        )

def make_entity(*args, **kwargs):
    return FraudCheckContext(*args, **kwargs)

def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)

def view(entity):
    return {
        'amount': entity.amount,
        'merchant_category': entity.merchant_category,
        'recent_count': entity.recent_count
    }

def new_service():
    return FraudService()
