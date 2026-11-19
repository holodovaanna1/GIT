from app.services.fraud_service import FraudService
from app.domain.risk_rules import LargeAmountRule, HighRiskMerchantRule

def build_service(rules=None):
    if rules is None:
        rules = (
            LargeAmountRule(),
            HighRiskMerchantRule()
        )
    return FraudService(rules)

