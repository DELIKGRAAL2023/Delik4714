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

def test_legacy_history():
    from app.domain.adapters import LegacyHistoryAdapter
    class Legacy:
        def make_rows(self,records,currency):return [{"key":"T1","count":1,"amount":money("10"),"status":"APPROVED"}]
    assert LegacyHistoryAdapter(Legacy()).build((),"EUR").approved_total==money("10")
