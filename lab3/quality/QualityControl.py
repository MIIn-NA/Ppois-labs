"""
Контроль качества - система контроля качества
"""
from datetime import datetime
from typing import List


class QualityControl:
    """Контроль качества"""

    def __init__(self, qc_id: str, name: str):
        self.qc_id = qc_id
        self.name = name
        self.factory = None
        self.inspectors = []
        self.products = []
        self.batches = []
        self.defect_reports = []
        self.quality_standards = {}
        self.total_inspections = 0
        self.total_passed = 0
        self.total_failed = 0
        self.created_at = datetime.now()

    def assign_to_factory(self, factory):
        """Назначить фабрике"""
        self.factory = factory
        factory.set_quality_control(self)

    def add_inspector(self, inspector):
        """Добавить инспектора"""
        self.inspectors.append(inspector)
        inspector.assign_to_quality_control(self)

    def add_product(self, product):
        """Добавить продукт"""
        self.products.append(product)

    def inspect_batch(self, batch, inspector):
        """Проверить партию"""
        self.batches.append(batch)
        self.total_inspections += 1
        batch.set_quality_control(self)

        # Простая проверка качества
        inspection_result = {
            'batch': batch,
            'inspector': inspector,
            'timestamp': datetime.now(),
            'passed': True  # по умолчанию проходит
        }

        if inspection_result['passed']:
            self.total_passed += 1
            batch.pass_quality_control()
        else:
            self.total_failed += 1

        return inspection_result

    def create_defect_report(self, product, defect_description: str, inspector):
        """Создать отчет о дефекте"""
        report = {
            'product': product,
            'defect': defect_description,
            'inspector': inspector,
            'timestamp': datetime.now(),
            'status': 'open'
        }
        self.defect_reports.append(report)
        return report

    def set_quality_standard(self, parameter: str, value):
        """Установить стандарт качества"""
        self.quality_standards[parameter] = value

    def get_pass_rate(self):
        """Получить процент прохождения"""
        if self.total_inspections == 0:
            return 0
        return (self.total_passed / self.total_inspections) * 100

    def get_defect_rate(self):
        """Получить процент дефектов"""
        if self.total_inspections == 0:
            return 0
        return (self.total_failed / self.total_inspections) * 100

    def get_open_defect_reports(self):
        """Получить открытые отчеты о дефектах"""
        return [r for r in self.defect_reports if r.get('status') == 'open']

    def __repr__(self):
        return f"QualityControl(name='{self.name}', pass_rate={self.get_pass_rate():.1f}%)"
