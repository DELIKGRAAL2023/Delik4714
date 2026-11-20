# ЛР5: стандартные зависимости пока создаёт сам сервис.
# Перенесите их сюда, сохранив явно переданные объекты.
from app.services.reporting_service import ReportingService
from app.support.types import Repository,choice
from app.domain.builders import TransactionHistoryReportBuilder,DeclinedTransactionsReportBuilder

def build_service(repository=None,builder=None,mode="history"):
    choices={"history":TransactionHistoryReportBuilder,"declined":DeclinedTransactionsReportBuilder}
    choice(mode,choices,"INVALID_CONFIG")
    builder=builder  # ЛР5: задайте реализацию по mode, если builder не передан
    return ReportingService(repository if repository is not None else Repository("transaction_id","DUPLICATE_TRANSACTION"),builder)
