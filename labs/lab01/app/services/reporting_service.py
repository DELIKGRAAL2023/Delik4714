from app.domain.reporting import Report, TransactionRecord
from app.support.types import ReportRow, currency, Repository
# Reporting service implementation

def make_entity(transaction_id, customer_id, merchant_id, amount, status, timestamp):
    return TransactionRecord(
        id=transaction_id,
        status=status,
        amount=amount,
    )


class ReportingService:

    def __init__(self, repository):
        self.repository = repository

    def record(self, transaction):
        return self.repository.add(transaction)

    def build(self, report_currency):
        code = currency(report_currency)

        rows = tuple(
            ReportRow(
                record.id,
                1,
                record.amount,
                record.status
            )
            for record in self.repository.all()
            if record.amount.currency == code
        )

        return Report(
            "История операций",
            code,
            rows
        )


def _new_legacy_service(repository):
    return ReportingService(repository)


def view(record):
    return record


def invoke(service, method, *args):
    if method == "record":
        return service.record(args[0])

    if method == "build":
        return service.build(args[0])

    raise ValueError(method)


def new_service(repository=None):
    return _new_legacy_service(
        repository if repository is not None
        else Repository(
            "id",
            "DUPLICATE_TRANSACTION"
        )
    )