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

def context(amount="100",category="RESTAURANT",recent=0):
    return api.make(money(amount),category,recent)

@pytest.mark.parametrize("amount,category,score,codes", [
 ("100","RESTAURANT",0,()),("1000","RESTAURANT",0,()),
 ("1000.01","RESTAURANT",40,("LARGE_AMOUNT",)),
 ("100","GAMBLING",40,("HIGH_RISK_MERCHANT",)),
 ("1000.01","GAMBLING",80,("LARGE_AMOUNT","HIGH_RISK_MERCHANT")),
])
def test_existing_risk(amount,category,score,codes):
    result=invoke(api.create(),"check",context(amount,category))
    assert (result.score,result.triggered_rules)==(score,codes)
    assert result.decision==("DECLINE" if score>=60 else "ALLOW")

def test_safe_after_risky_and_context_unchanged():
    service=api.create()
    safe=context()
    before=api.view(safe)
    invoke(service,"check",context("2000","GAMBLING"))
    result=invoke(service,"check",safe)
    assert result.score==0 and result.triggered_rules==()
    assert api.view(safe)==before

from app.domain.fraud import FraudResult

@pytest.mark.parametrize("recent",[-1,1.5,True])
def test_invalid_count(recent):
    error("INVALID_CONTEXT",lambda:context(recent=recent))

def test_currency_and_positive_amount():
    error("CURRENCY_MISMATCH",lambda:api.make(money("1","USD"),"RESTAURANT",0))
    error("INVALID_AMOUNT",lambda:context("0"))

@pytest.mark.parametrize("score",[-1,101,True,1.5])
def test_invalid_score(score):
    error("INVALID_RESULT",lambda:FraudResult(score,()))

def test_decision_boundary_and_snapshot():
    codes=["X"]
    result=FraudResult(60,codes)
    codes.clear()
    assert result.triggered_rules==("X",)
    assert result.decision=="DECLINE"
    assert FraudResult(59,()).decision=="ALLOW"

from app.domain.risk_rules import FraudRule,LargeAmountRule,HighRiskMerchantRule

def test_abc_is_abstract():
    with pytest.raises(TypeError): FraudRule()

def test_rule_contributions():
    assert LargeAmountRule().evaluate(context("1000"))==0
    assert LargeAmountRule().evaluate(context("1000.01"))==40
    assert HighRiskMerchantRule().evaluate(context(category="GAMBLING"))==40

def test_rules_used_in_real_path(monkeypatch):
    monkeypatch.setattr(HighRiskMerchantRule,"evaluate",lambda *args:60)
    result=invoke(api.create(),"check",context())
    assert result.score==60 and result.decision=="DECLINE"
