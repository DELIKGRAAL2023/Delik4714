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

STAMP=datetime(2030,5,1,tzinfo=timezone.utc)

def record(key="T1",amount="10",status="APPROVED",merchant="M1",code="EUR"):
    return api.make(key,"C1",merchant,money(amount,code),status,STAMP)

def prepared(mode=None):
    service=api.create() if mode is None else api.create(mode=mode)
    for item in (record(),record("T2","20","DECLINED"),record("T3","5"),record("T4","99",code="USD")):
        invoke(service,"record",item)
    return service

def test_history_ignores_declines_in_total_and_other_currency():
    service=prepared()
    report=invoke(service,"build","EUR")
    assert report.title=="История операций"
    assert [row.key for row in report.rows]==["T1","T2","T3"]
    assert report.approved_total==money("15")
    assert report.rows[1].amount==money("20")
    assert invoke(service,"build","EUR")==report

def test_new_repository_empty_with_explicit_currency():
    invoke(prepared(),"build","EUR")
    report=invoke(api.create(),"build","USD")
    assert report.rows==() and report.approved_total==money("0","USD")

from app.domain.reporting import TransactionRecord,Report
from app.support.types import ReportRow

def test_record_invariants():
    error("INVALID_AMOUNT",lambda:record(amount="0"))
    error("INVALID_STATUS",lambda:record(status="PENDING"))
    item=record()
    with pytest.raises((AttributeError,TypeError)):item.status="DECLINED"

def test_report_copies_rows_and_checks_currency():
    row=ReportRow("T",1,money("10"),"APPROVED")
    rows=[row]
    report=Report("R","EUR",rows)
    rows.clear()
    assert report.rows==(row,)
    error("CURRENCY_MISMATCH",lambda:Report("R","USD",[row]))

def test_duplicate_record_is_not_new_spending():
    service=prepared()
    error("DUPLICATE_TRANSACTION",lambda:service.record(record()))
    assert service.build("EUR").approved_total==money("15")
