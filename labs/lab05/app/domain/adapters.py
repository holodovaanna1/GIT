from app.domain.risk_rules import FraudRule

class LegacyRiskAdapter(FraudRule):
    code="LEGACY_RISK"
    def __init__(self,legacy):
        self._legacy=legacy
    def evaluate(self,context):
        raise NotImplementedError("Бонус: локальный адаптер")
