import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.reporting import TransactionRecord
from app.support.types import money

def test_progression_report_currency_and_snapshot():
    service = api.create()
    stamp = datetime(2030, 5, 1, tzinfo=timezone.utc)
    first = TransactionRecord("T1", "C", "M", money("10"), "APPROVED", stamp)
    service.record(first)
    old = service.build("EUR")
    code("DUPLICATE_TRANSACTION", lambda: service.record(first))
    service.record(TransactionRecord("T2", "C", "M", money("7", "USD"), "APPROVED", stamp))
    assert service.build("USD").approved_total == money("7", "USD")
    assert service.build("EUR").approved_total == old.approved_total == money("10")
    assert len(old.rows) == 1

from app.domain.builders import ReportBuilder
from app.domain.reporting import Report

def test_progression_false_builder_error_preserves_records():
    calls = []
    class Once(ReportBuilder):
        def __bool__(self): return False
        def build(self, records, currency):
            calls.append((records, currency))
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return Report("CONTROL", currency, ())
    service = api.create(builder=Once())
    item = TransactionRecord("T", "C", "M", money("1"), "APPROVED", datetime(2030,5,1,tzinfo=timezone.utc))
    service.record(item)
    code("TEMPORARY", lambda: service.build("EUR"))
    assert len(calls) == 1
    assert service.build("EUR").title == "CONTROL"
    assert calls == [((item,), "EUR"), ((item,), "EUR")]

from app.support.types import money

def test_progression_extra_lab05():
    service = api.create()
    reports = service.build_many(("EUR", "USD", "EUR"))
    assert tuple(reports) == ("EUR", "USD")
    assert reports["EUR"].currency == "EUR"
    assert service.approved_totals(("EUR", "USD")) == {"EUR": money("0"), "USD": money("0", "USD")}
