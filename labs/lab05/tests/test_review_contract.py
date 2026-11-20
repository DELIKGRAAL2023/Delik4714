import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

@pytest.mark.parametrize("stamp",[datetime(2030,5,1),datetime(2030,5,1,tzinfo=timezone(timedelta(hours=1)))])
def test_review_record_requires_explicit_utc(stamp):
    assert_code("INVALID_TIMESTAMP",lambda:api.make("T","C","M",money("1"),"APPROVED",stamp))

def test_review_builder_wrong_currency_is_not_accepted():
    from app.domain.reporting import Report
    from app.domain.builders import ReportBuilder
    from app.services.reporting_service import ReportingService
    from app.support.types import Repository
    class Wrong(ReportBuilder):
        def build(self,records,code):return Report("R","USD",())
    assert_code("INVALID_REPORT",lambda:ReportingService(Repository("transaction_id"),Wrong()).build("EUR"))
