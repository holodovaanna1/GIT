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


<<<<<<< HEAD
=======
def make_entity(amount, merchant_category, recent_count=0):
    return dict(amount=amount, merchant_category=merchant_category, recent_count=recent_count)

def view(context):
    return dict(context)


def invoke(service, method, context):
    if method != "check":
        raise ValueError(method)

    if isinstance(context, dict):
        context = FraudCheckContext(
            amount=context["amount"],
            currency=context.get("currency", "EUR"),
            category=context.get("merchant_category", "UNKNOWN")
        )

    return service.check(context)


>>>>>>> 1f6449d4acb80832c818dddfa2fb0a61d270f8bc
def new_service():
    return FraudService()
