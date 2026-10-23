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

def test_remaining():
    from app.domain.fraud import FraudResult
    assert FraudResult(59,()).remaining_to_decline()==1
    assert FraudResult(80,()).remaining_to_decline()==0
