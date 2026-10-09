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
