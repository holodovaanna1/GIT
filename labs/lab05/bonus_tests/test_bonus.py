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

def test_legacy_risk():
    from app.domain.fraud import FraudCheckContext
    from app.domain.adapters import LegacyRiskAdapter
    class Legacy:
        def score(self,amount,category):return 60 if category=="GAMBLING" else 0
    assert LegacyRiskAdapter(Legacy()).evaluate(FraudCheckContext(money("1"),"GAMBLING",0))==60
