from dataclasses import dataclass

from app.support.types import (
    identifier,
    choice,
    Money,
    ReportRow,
    total_money,
)
from app.support.types import currency as valid_currency
from app.support.errors import DomainError


# ЛР1: TransactionRecord вместо словаря.

@dataclass(frozen=True)
class TransactionRecord:
    id: str
    status: str
    amount: Money

    def __post_init__(self):
        identifier(self.id)
        choice(self.status, ("APPROVED", "DECLINED"))

        if not isinstance(self.amount, Money):
            raise DomainError("INVALID_AMOUNT")


@dataclass(frozen=True)
class Report:
    title: str
    currency: str
    rows: tuple

    def __post_init__(self):
        valid_currency(self.currency)

        rows = tuple(self.rows)

        if any(not isinstance(row, ReportRow) for row in rows):
            raise DomainError("INVALID_REPORT")

        if any(row.amount.currency != self.currency for row in rows):
            raise DomainError("CURRENCY_MISMATCH")

        object.__setattr__(self, "rows", rows)

    @property
    def approved_total(self):
        return total_money(
            (
                row.amount
                for row in self.rows
                if row.status != "DECLINED"
            ),
            self.currency,
        )