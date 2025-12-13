"""
Заявка на материалы - запрос материалов со склада
"""
from datetime import datetime


class MaterialRequest:
    """Заявка на материалы"""

    def __init__(self, request_id: str, quantity: float):
        self.request_id = request_id
        self.quantity = quantity
        self.raw_material = None
        self.production_line = None
        self.warehouse = None
        self.created_at = datetime.now()
        self.fulfilled_at = None
        self.status = "pending"  # pending, approved, fulfilled, rejected

    def set_raw_material(self, material):
        """Установить сырье"""
        self.raw_material = material
        material.create_material_request(self)

    def set_production_line(self, production_line):
        """Установить производственную линию"""
        self.production_line = production_line

    def set_warehouse(self, warehouse):
        """Установить склад"""
        self.warehouse = warehouse

    def approve(self):
        """Одобрить заявку"""
        self.status = "approved"
        return {'request': self.request_id, 'approved_at': datetime.now()}

    def fulfill(self):
        """Выполнить заявку"""
        self.status = "fulfilled"
        self.fulfilled_at = datetime.now()
        if self.raw_material:
            self.raw_material.reduce_stock(self.quantity)
        return {'request': self.request_id, 'fulfilled_at': self.fulfilled_at}

    def reject(self, reason: str):
        """Отклонить заявку"""
        self.status = "rejected"
        return {'request': self.request_id, 'rejected_at': datetime.now(), 'reason': reason}

    def get_estimated_cost(self):
        """Получить расчетную стоимость"""
        if self.raw_material and hasattr(self.raw_material, 'unit_price'):
            return self.quantity * self.raw_material.unit_price
        return 0

    def is_fulfilled(self):
        """Проверить, выполнена ли заявка"""
        return self.status == "fulfilled"

    def __repr__(self):
        return f"MaterialRequest(id='{self.request_id}', quantity={self.quantity}, status='{self.status}')"
