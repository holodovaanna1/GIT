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
