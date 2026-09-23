from app.domain.fraud import FraudResult


def make_entity(amount, merchant_category, recent_count=0):
    return dict(amount=amount, merchant_category=merchant_category, recent_count=recent_count)


def _new_legacy_service():
    return {}


def view(context):
    return dict(context)


def invoke(service, method, context):
    if method != "check":
        raise ValueError(method)
    score, codes = 0, []
    if context["amount"].amount > 1000:
        score += 40
        codes.append("LARGE_AMOUNT")
    if context["merchant_category"] == "GAMBLING":
        score += 40
        codes.append("HIGH_RISK_MERCHANT")
    return FraudResult(score, tuple(codes))



def new_service():
    return _new_legacy_service()
