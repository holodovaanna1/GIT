from app.domain.fraud import FraudCheckContext, FraudResult
from app.domain.risk_rules import LargeAmountRule, HighRiskMerchantRule
from app.support.errors import DomainError
from app.support.types import risk_points


class FraudService:
    def __init__(self, rules=()):
        self._rules = [LargeAmountRule(), HighRiskMerchantRule()]
        self._codes = []  # ЛР5: накопление между вызовами одного экземпляра

    def check(self, context):
        raise NotImplementedError("ЛР5: реализуйте FraudService.check по TASK.md")

    def check_many(self, contexts):
        raise NotImplementedError("ЛР5: реализуйте FraudService.check_many по TASK.md")

    def highest_risk(self, contexts):
        raise NotImplementedError("ЛР5: реализуйте FraudService.highest_risk по TASK.md")

def make_entity(*args, **kwargs):
    return FraudCheckContext(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'amount': entity.amount, 'merchant_category': entity.merchant_category, 'recent_count': entity.recent_count}
