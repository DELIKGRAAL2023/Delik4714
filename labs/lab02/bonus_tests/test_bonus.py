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

def test_count_not_number_of_rows():
    from app.domain.reporting import Report
    from app.support.types import ReportRow
    assert Report("R","EUR",[ReportRow("M1",3,money("10"),None)]).transaction_count==3
