from app.domain.fraud import FraudCheckContext, FraudResult

class FraudService:
    

    def check(self, context: FraudCheckContext) -> FraudResult:
        
        score = 0
        codes = []

        if context.amount.amount > 1000:
            score += 40
            codes.append("LARGE_AMOUNT")

        if context.category == "GAMBLING":
            score += 40
            codes.append("HIGH_RISK_MERCHANT")

        return FraudResult(score, tuple(codes))


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

def new_service():
    return FraudService()
