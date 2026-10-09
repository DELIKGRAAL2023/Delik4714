from dataclasses import dataclass
from app.support.types import identifier,positive,choice,utc_seconds,Money,ReportRow,total_money
from app.support.types import currency as valid_currency
from app.support.errors import DomainError


@dataclass(frozen=True)
class TransactionRecord:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Money
    status: str
    timestamp: object

    def __post_init__(self):
        
        identifier(self.transaction_id)
        identifier(self.customer_id)
        identifier(self.merchant_id)
        
        if self.amount.amount <= 0:
            raise DomainError("INVALID_AMOUNT")

        if self.status not in {"APPROVED", "DECLINED"}:
            raise DomainError("INVALID_STATUS")
        
        utc_seconds(self.timestamp)


@dataclass(frozen=True)
class Report:
    title: str
    currency: str
    rows: tuple

    def __post_init__(self):
        valid_currency(self.currency)

        object.__setattr__(self, "rows", tuple(self.rows))

        for row in self.rows:
            if row.amount.currency != self.currency:
                raise DomainError("CURRENCY_MISMATCH")
                
        rows=tuple(self.rows)
        if any(not isinstance(row,ReportRow) for row in rows):
            raise DomainError("INVALID_REPORT")
          # ЛР2: снимок коллекции

    @property
    def approved_total(self):
        return total_money((row.amount for row in self.rows if row.status != "DECLINED"),self.currency)
