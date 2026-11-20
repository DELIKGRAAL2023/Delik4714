from app.domain.builders import ReportBuilder
from app.domain.reporting import Report
from app.support.types import legacy_rows

class LegacyHistoryAdapter(ReportBuilder):
    def __init__(self,legacy):self._legacy=legacy
    def build(self,records,currency):
        raise NotImplementedError("Бонус: локальные строки")
