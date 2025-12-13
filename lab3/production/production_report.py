"""
Отчет о производстве - статистика производства
"""
from datetime import datetime
from typing import List


class ProductionReport:
    """Отчет о производстве"""

    def __init__(self, report_id: str, period_start: datetime, period_end: datetime):
        self.report_id = report_id
        self.period_start = period_start
        self.period_end = period_end
        self.production_line = None
        self.batches = []
        self.manager = None
        self.production_plan = None
        self.total_produced = 0
        self.total_defects = 0
        self.generated_at = datetime.now()

    def set_production_line(self, production_line):
        """Установить производственную линию"""
        self.production_line = production_line

    def add_batch(self, batch):
        """Добавить партию"""
        self.batches.append(batch)
        self.total_produced += batch.quantity

    def set_manager(self, manager):
        """Установить менеджера"""
        self.manager = manager
        manager.submit_report(self)

    def link_production_plan(self, plan):
        """Связать с планом производства"""
        self.production_plan = plan

    def add_defect_count(self, count: int):
        """Добавить количество дефектов"""
        self.total_defects += count

    def calculate_quality_rate(self):
        """Рассчитать процент качества"""
        if self.total_produced == 0:
            return 0
        return ((self.total_produced - self.total_defects) / self.total_produced) * 100

    def calculate_efficiency(self):
        """Рассчитать эффективность"""
        if not self.production_plan or self.production_plan.target_volume == 0:
            return 0
        return (self.total_produced / self.production_plan.target_volume) * 100

    def get_summary(self):
        """Получить сводку отчета"""
        return {
            'report_id': self.report_id,
            'period': f"{self.period_start} - {self.period_end}",
            'production_line': self.production_line.name if self.production_line else None,
            'total_produced': self.total_produced,
            'total_defects': self.total_defects,
            'quality_rate': self.calculate_quality_rate(),
            'batches_count': len(self.batches),
            'generated_at': self.generated_at
        }

    def __repr__(self):
        return f"ProductionReport(id='{self.report_id}', produced={self.total_produced})"
