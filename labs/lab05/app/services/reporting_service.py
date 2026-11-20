from app.domain.reporting import TransactionRecord
from app.support.types import validate_report, currency



class ReportingService:
    def __init__(self, repository, builder):
        self._repository = repository
        self._builder = builder

    def record(self, record):
        return self._repository.add(record)

    def build(self, code):
        currency(code)
        records = self._repository.all()
        result = self._builder.build(records, code)
        return validate_report(result, code)

    def build_many(self, currencies):
        return {
            code: self.build(code)
            for code in dict.fromkeys(currencies)
        }

    def approved_totals(self, currencies):
        reports = self.build_many(currencies)
        return {
            code: report.approved_total
            for code, report in reports.items()
        }


def make_entity(*args, **kwargs):
    return TransactionRecord(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'transaction_id': entity.transaction_id, 'customer_id': entity.customer_id, 'merchant_id': entity.merchant_id, 'amount': entity.amount, 'status': entity.status, 'timestamp': entity.timestamp}
