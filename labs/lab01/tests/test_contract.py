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
