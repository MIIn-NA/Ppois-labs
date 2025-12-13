"""
Поставка - доставка от поставщика
"""
from datetime import datetime
from typing import List


class Delivery:
    """Поставка"""

    def __init__(self, delivery_id: str, scheduled_date: datetime):
        self.delivery_id = delivery_id
        self.scheduled_date = scheduled_date
        self.purchase_order = None
        self.supplier = None
        self.raw_materials = []
        self.warehouse = None
        self.delivered_at = None
        self.status = "scheduled"  # scheduled, in_transit, delivered, failed
        self.tracking_number = None

    def set_purchase_order(self, purchase_order):
        """Установить заказ на закупку"""
        self.purchase_order = purchase_order
        purchase_order.set_delivery(self)

    def set_supplier(self, supplier):
        """Установить поставщика"""
        self.supplier = supplier

    def add_raw_material(self, material, quantity: float):
        """Добавить сырье"""
        self.raw_materials.append({
            'material': material,
            'quantity': quantity
        })

    def set_warehouse(self, warehouse):
        """Установить склад"""
        self.warehouse = warehouse

    def set_tracking_number(self, tracking: str):
        """Установить номер отслеживания"""
        self.tracking_number = tracking

    def start_transit(self):
        """Начать доставку"""
        self.status = "in_transit"
        return {'delivery': self.delivery_id, 'started_at': datetime.now()}

    def complete_delivery(self):
        """Завершить поставку"""
        self.status = "delivered"
        self.delivered_at = datetime.now()

        # Добавить материалы на склад
        if self.warehouse:
            for item in self.raw_materials:
                item['material'].add_stock(item['quantity'])

        if self.purchase_order:
            self.purchase_order.mark_delivered()

        return {'delivery': self.delivery_id, 'delivered_at': self.delivered_at}

    def fail_delivery(self, reason: str):
        """Провалить поставку"""
        self.status = "failed"
        return {'delivery': self.delivery_id, 'failed_at': datetime.now(), 'reason': reason}

    def is_delayed(self):
        """Проверить, задержана ли поставка"""
        if self.status != "delivered" and datetime.now() > self.scheduled_date:
            return True
        return False

    def get_total_quantity(self):
        """Получить общее количество материалов"""
        return sum(item['quantity'] for item in self.raw_materials)

    def __repr__(self):
        return f"Delivery(id='{self.delivery_id}', status='{self.status}')"
