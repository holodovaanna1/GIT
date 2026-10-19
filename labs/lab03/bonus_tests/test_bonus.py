import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError
from app.support.types import Repository, CheckResult, Money, money


def error(code, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == code


def invoke(service, method, *args, **kwargs):
    return api.call(service, method, *args, **kwargs)

def test_rule_parameters():
    from app.domain.fraud import FraudCheckContext
    from app.domain.risk_rules import LargeAmountRule
    rule=LargeAmountRule(threshold=money("50"),points=60)
    assert rule.evaluate(FraudCheckContext(money("50.01"),"RESTAURANT",0))==60
    error("INVALID_CONFIG",lambda:LargeAmountRule(points=0))
