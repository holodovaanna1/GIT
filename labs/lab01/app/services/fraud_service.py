from app.domain.fraud import FraudResult


class FraudCheckContext:
    def __init__(self, amount, merchant_category, recent_count=0):
        self.amount = amount
        self.merchant_category = merchant_category
        self.recent_count = recent_count


class FraudService:
    def check(self, context: FraudCheckContext) -> FraudResult:
        score = 0
        codes = []
        if context.amount.amount > 1000:
            score += 40
            codes.append("LARGE_AMOUNT")
        if context.merchant_category == "GAMBLING":
            score += 40
            codes.append("HIGH_RISK_MERCHANT")
        return FraudResult(score, tuple(codes))


def new_service():
    return FraudService()





