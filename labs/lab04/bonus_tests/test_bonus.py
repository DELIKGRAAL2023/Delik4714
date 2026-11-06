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

def test_currency_diagnostic_uses_validated_report():
    class ReportLike:
        currency="EUR"
        @property
        def rows(self):raise AssertionError("Повторный обход строк не нужен")
    assert api.create().currency_diagnostic(ReportLike())=="EUR"
