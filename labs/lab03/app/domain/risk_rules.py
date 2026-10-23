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
        if context.amount.amount > 1000:
            return 40
        return 0


class HighRiskMerchantRule(FraudRule):
    code = "HIGH_RISK_MERCHANT"

    def evaluate(self, context):
        if context.merchant_category == "GAMBLING":
            return 40
        return 0
      
class ManyRecentAttemptsRule(FraudRule):
    code = "MANY_RECENT_ATTEMPTS"
    def evaluate(self, context):
        if context.recent_count >= 3:
            return 20
        return 0
