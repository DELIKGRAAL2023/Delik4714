from app.domain.reporting import TransactionRecord,Report
from app.support.types import currency,select_records,record_row


class ReportingService:
    def __init__(self,repository,mode="history"):
        self._repository=repository
        self._mode=mode

    def record(self,record):return self._repository.add(record)

    def build(self,code):
        status="DECLINED" if self._mode=="declined" else None
        title="Отклонённые операции" if status else "История операций"
        rows=tuple(record_row(record) for record in select_records(self._repository.all(),code,status))
        return Report(title,code,rows)

def make_entity(*args, **kwargs):
    return TransactionRecord(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'transaction_id': entity.transaction_id, 'customer_id': entity.customer_id, 'merchant_id': entity.merchant_id, 'amount': entity.amount, 'status': entity.status, 'timestamp': entity.timestamp}


from app.support.types import Repository,choice

def new_service(repository=None,mode="history"):
    choice(mode,("history","declined"),"INVALID_CONFIG")
    return ReportingService(repository if repository is not None else Repository("transaction_id","DUPLICATE_TRANSACTION"),mode)
