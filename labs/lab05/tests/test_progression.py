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

from app.domain.risk_rules import FraudRule
from app.services.fraud_service import FraudService

def test_progression_dependency_error_then_success_does_not_accumulate():
    calls = []
    class Once(FraudRule):
        code = "CONTROL"
        def evaluate(self, context):
            calls.append(context)
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return 11
    rules = [Once()]
    service = FraudService(rules)
    rules.clear()
    context = FraudCheckContext(money("1"), "RESTAURANT", 0)
    code("TEMPORARY", lambda: service.check(context))
    assert len(calls) == 1
    result = service.check(context)
    assert result.score == 11 and result.triggered_rules == ("CONTROL",) and len(calls) == 2

from app.services.fraud_service import FraudService
from app.domain.fraud import FraudResult

def test_progression_extra_lab05(monkeypatch):
    calls = []
    def check(self, score):
        calls.append(score)
        return FraudResult(score, ())
    monkeypatch.setattr(FraudService, "check", check)
    service = object.__new__(FraudService)
    assert tuple(r.score for r in service.check_many([10, 70, 20])) == (10, 70, 20)
    winner = service.highest_risk([10, 70, 70])
    assert winner[0] == 1 and winner[1].score == 70
    assert service.highest_risk([]) is None
    assert calls == [10, 70, 20, 10, 70, 70]
