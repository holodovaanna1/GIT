from app.domain.fraud import FraudCheckContext, FraudResult
from app.support.errors import DomainError
from app.support.types import risk_points

class FraudService:
    def __init__(self, rules=()):
        self._rules = tuple(rules)

    def check(self, context):
        if not isinstance(context, FraudCheckContext):
            raise DomainError("INVALID_CONTEXT")
        score = 0
        codes = []
        for rule in self._rules:
            points = risk_points(rule.evaluate(context))

            if points > 0:
                score = min(100, score + points)

                if rule.code not in codes:
                    codes.append(rule.code)

        return FraudResult(
            score=score,
            triggered_rules=tuple(codes)
        )

    def check_many(self, contexts):
        return tuple(self.check(context) for context in contexts)

    def highest_risk(self, contexts):
        results = self.check_many(contexts)

        if not results:
            return None

        best_index = 0
        best_result = results[0]

        for index, result in enumerate(results[1:], start=1):
            if result.score > best_result.score:
                best_index = index
                best_result = result

        return best_index, best_result
    
def make_entity(*args, **kwargs):
    return FraudCheckContext(*args, **kwargs)

def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)

def view(entity):
    return {
        'amount': entity.amount,
        'merchant_category': entity.merchant_category,
        'recent_count': entity.recent_count
    }
