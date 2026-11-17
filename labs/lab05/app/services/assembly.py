# ЛР5: стандартные зависимости пока создаёт сам сервис.
# Перенесите их сюда, сохранив явно переданные объекты.
from app.services.fraud_service import FraudService
from app.domain.risk_rules import LargeAmountRule, HighRiskMerchantRule

def build_service(rules=None):
    return FraudService(() if rules is None else rules)
