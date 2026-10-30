import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.fraud import FraudCheckContext
from app.support.types import money

def test_progression_risk_does_not_accumulate():
    service = api.create()
    safe = FraudCheckContext(money("10"), "RESTAURANT", 0)
    risky = FraudCheckContext(money("1001"), "GAMBLING", 0)
    first = service.check(safe)
    denial = service.check(risky)
    third = service.check(safe)
    assert first.score == third.score == 0
    assert first.decision == third.decision == "ALLOW"
    assert denial.score == 80 and denial.decision == "DECLINE"
    assert first.triggered_rules == third.triggered_rules == ()
