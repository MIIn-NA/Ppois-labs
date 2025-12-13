"""
Производственный заказ - заказ на производство партии
"""
from datetime import datetime
from typing import List


class ProductionOrder:
    """Производственный заказ"""

    def __init__(self, order_id: str, quantity: int):
        self.order_id = order_id
        self.quantity = quantity
        self.production_line = None
        self.product = None
        self.customer_order = None
        self.raw_materials = []
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.status = "pending"  # pending, in_progress, completed, cancelled
        self.produced_quantity = 0

    def assign_production_line(self, production_line):
        """Назначить производственную линию"""
        self.production_line = production_line
        production_line.create_production_order(self)

    def assign_product(self, product):
        """Назначить продукт"""
        self.product = product

    def link_customer_order(self, order):
        """Связать с заказом клиента"""
        self.customer_order = order

    def add_raw_material(self, material, quantity: float):
        """Добавить сырье"""
        self.raw_materials.append({
            'material': material,
            'quantity': quantity
        })

    def start_production(self):
        """Начать производство"""
        self.status = "in_progress"
        self.started_at = datetime.now()
        return {'order': self.order_id, 'started_at': self.started_at}

    def complete_production(self):
        """Завершить производство"""
        self.status = "completed"
        self.completed_at = datetime.now()
        self.produced_quantity = self.quantity
        return {'order': self.order_id, 'completed_at': self.completed_at}

    def cancel(self, reason: str):
        """Отменить заказ"""
        self.status = "cancelled"
        return {'order': self.order_id, 'cancelled_at': datetime.now(), 'reason': reason}

    def update_produced_quantity(self, quantity: int):
        """Обновить произведенное количество"""
        self.produced_quantity = quantity

    def get_completion_percentage(self):
        """Получить процент выполнения"""
        if self.quantity == 0:
            return 0
        return (self.produced_quantity / self.quantity) * 100

    def __repr__(self):
        return f"ProductionOrder(id='{self.order_id}', quantity={self.quantity}, status='{self.status}')"
