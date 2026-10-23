from abc import ABC, abstractmethod
from app.domain.reporting import Report
from app.support.types import select_records, record_row


class ReportBuilder(ABC):
    @abstractmethod
    def build(self, records, currency):
        raise NotImplementedError


class TransactionHistoryReportBuilder(ReportBuilder):
    
    def __init__(self, title="История операций"):
        self.title = title
     
    def build(self, records, currency):
        rows = tuple(
            record_row(record)
            for record in select_records(records, currency)
        )
        return Report(self.title, currency, rows)


class DeclinedTransactionsReportBuilder(ReportBuilder):
    def build(self, records, currency):
        rows = tuple(
            record_row(record)
            for record in select_records(records, currency, "DECLINED")
        )
        return Report("Отклонённые операции", currency, rows)