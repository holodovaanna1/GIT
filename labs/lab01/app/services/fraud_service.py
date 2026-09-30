from app.support.types import Money, positive
from app.support.errors import DomainError
from app.domain.fraud import FraudResult


class FraudCheckContext:
    def __init__(self, amount: Money, category: str, recent_count: int = 0):
        positive(amount)
        if not category or not category.strip():
            raise DomainError("INVALID_CONTEXT")
        self.amount = amount
        self.category = category
        self.recent_count = recent_count


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


def make_entity(amount, category, recent_count=0):
    return FraudCheckContext(amount, category, recent_count)


def view(context):
    return {
        "amount": context.amount,
        "category": context.category,
        "recent_count": context.recent_count,
    }


def invoke(service, method, context):
    if method != "check":
        raise ValueError(method)
    if isinstance(context, dict):
        context = FraudCheckContext(
            amount=context["amount"],
            category=context.get("category") or context.get("merchant_category", "UNKNOWN"),
            recent_count=context.get("recent_count", 0),
        )
    return service.check(context)


def new_service():
    return FraudService()





