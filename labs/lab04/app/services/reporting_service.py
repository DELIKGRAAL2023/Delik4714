from app.domain.reporting import TransactionRecord,Report
from app.domain.builders import TransactionHistoryReportBuilder,DeclinedTransactionsReportBuilder
from app.support.types import validate_report,currency,select_records,record_row,total_money


class ReportingService:
    def __init__(self,repository,builder):
        self._repository=repository
        self._builder=builder

    def record(self,record):
        return self._repository.add(record)

    def build(self,code):
        currency(code)
        if isinstance(self._builder,DeclinedTransactionsReportBuilder):
            rows=tuple(record_row(record) for record in select_records(self._repository.all(),code,"DECLINED"))
            result=Report("Отклонённые операции",code,rows)
        else:
            result=self._builder.build(self._repository.all(),code)
        self._last_total=total_money((row.amount for row in result.rows if row.status!="DECLINED"),code)
        return validate_report(result,code)

    def currency_diagnostic(self,report):
        return report.rows[0].amount.currency if report.rows else report.currency

def make_entity(*args, **kwargs):
    return TransactionRecord(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'transaction_id': entity.transaction_id, 'customer_id': entity.customer_id, 'merchant_id': entity.merchant_id, 'amount': entity.amount, 'status': entity.status, 'timestamp': entity.timestamp}


from app.support.types import Repository,choice
from app.domain.builders import TransactionHistoryReportBuilder,DeclinedTransactionsReportBuilder

def new_service(repository=None,builder=None,mode="history"):
    choices={"history":TransactionHistoryReportBuilder,"declined":DeclinedTransactionsReportBuilder}
    choice(mode,choices,"INVALID_CONFIG")
    builder=choices[mode]() if builder is None else builder
    return ReportingService(repository if repository is not None else Repository("transaction_id","DUPLICATE_TRANSACTION"),builder)
