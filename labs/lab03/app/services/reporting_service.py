
from app.domain.reporting import TransactionRecord
from app.domain.builders import (
    TransactionHistoryReportBuilder,
    DeclinedTransactionsReportBuilder,
)
from app.support.types import (
    currency,
    validate_report,
    Repository,
    choice,
)


class ReportingService:
    def __init__(self, repository, builder):
        self._repository = repository
        self.builder = builder

    def record(self, record):
        return self._repository.add(record)

    def build(self, code):
        code = currency(code)
        records = tuple(self._repository.all())

        result = self.builder.build(records, code)
        validate_report(result, code)

        return result


def make_entity(*args, **kwargs):
    return TransactionRecord(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {
        "transaction_id": entity.transaction_id,
        "customer_id": entity.customer_id,
        "merchant_id": entity.merchant_id,
        "amount": entity.amount,
        "status": entity.status,
        "timestamp": entity.timestamp,
    }


def new_service(repository=None, mode="history"):
    choice(mode, ("history", "declined"), "INVALID_CONFIG")

    if repository is None:
        repository = Repository(
            "transaction_id",
            "DUPLICATE_TRANSACTION",
        )

    if mode == "history":
        builder = TransactionHistoryReportBuilder()
    else:
        builder = DeclinedTransactionsReportBuilder()

    return ReportingService(repository, builder)
