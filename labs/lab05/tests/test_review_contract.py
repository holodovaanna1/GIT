import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

def test_review_result_codes_must_be_nonempty_and_unique():
    from app.domain.fraud import FraudResult
    assert_code("INVALID_RESULT",lambda:FraudResult(40,("X","X")))
    assert_code("INVALID_RESULT",lambda:FraudResult(40,("",)))

def test_review_all_contributions_are_evaluated_even_at_cap():
    from app.domain.fraud import FraudCheckContext
    from app.domain.risk_rules import FraudRule
    from app.services.fraud_service import FraudService
    calls=[]
    class Contribution(FraudRule):
        def __init__(self,code,points):self.code,self.points=code,points
        def evaluate(self,item):calls.append(self.code);return self.points
    context = FraudCheckContext(money("1"),"RESTAURANT",0)
    result=FraudService([Contribution("A",100),Contribution("ZERO",0),Contribution("B",1)]).check(context)
    assert result.score == 100 and result.triggered_rules == ("A","B")
    assert calls == ["A","ZERO","B"]
