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
