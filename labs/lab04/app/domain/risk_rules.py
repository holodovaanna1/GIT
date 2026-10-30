from abc import ABC, abstractmethod
from app.support.types import money, decimal_value
from app.support.errors import DomainError


class FraudRule(ABC):
    code = ""

    @abstractmethod
    def evaluate(self, context):
        raise NotImplementedError


class LargeAmountRule(FraudRule):
    code = "LARGE_AMOUNT"

    def evaluate(self, context):
        return 40 if context.amount.amount > 1000 else 0


class HighRiskMerchantRule(FraudRule):
    code = "HIGH_RISK_MERCHANT"

    def evaluate(self, context):
        return 40 if context.merchant_category == "GAMBLING" else 0
