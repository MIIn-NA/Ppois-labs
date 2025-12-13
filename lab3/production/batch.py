"""
Партия продукции - произведенная партия товара
"""
from datetime import datetime


class Batch:
    """Партия продукции"""

    def __init__(self, batch_id: str, quantity: int):
        self.batch_id = batch_id
        self.quantity = quantity
        self.product = None
        self.production_order = None
        self.quality_control = None
        self.warehouse = None
        self.produced_at = datetime.now()
        self.quality_status = "pending"  # pending, passed, failed
        self.is_stored = False

    def assign_product(self, product):
        """Назначить продукт"""
        self.product = product

    def link_production_order(self, production_order):
        """Связать с производственным заказом"""
        self.production_order = production_order

    def set_quality_control(self, quality_control):
        """Установить контроль качества"""
        self.quality_control = quality_control

    def pass_quality_control(self):
        """Пройти контроль качества"""
        self.quality_status = "passed"
        return {'batch': self.batch_id, 'quality_status': 'passed', 'timestamp': datetime.now()}

    def fail_quality_control(self, reason: str):
        """Не пройти контроль качества"""
        self.quality_status = "failed"
        return {'batch': self.batch_id, 'quality_status': 'failed', 'reason': reason, 'timestamp': datetime.now()}

    def store_in_warehouse(self, warehouse):
        """Сохранить на складе"""
        self.warehouse = warehouse
        self.is_stored = True
        return {'batch': self.batch_id, 'warehouse': warehouse.name if hasattr(warehouse, 'name') else str(warehouse)}

    def get_age_days(self):
        """Получить возраст партии в днях"""
        delta = datetime.now() - self.produced_at
        return delta.days

    def is_quality_approved(self):
        """Проверить, одобрена ли партия"""
        return self.quality_status == "passed"

    def __repr__(self):
        return f"Batch(id='{self.batch_id}', quantity={self.quantity}, quality='{self.quality_status}')"
