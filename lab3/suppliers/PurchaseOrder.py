"""
Заказ на закупку - заказ поставщику
"""
from datetime import datetime
from typing import List


class PurchaseOrder:
    """Заказ на закупку"""

    def __init__(self, order_id: str, order_date: datetime):
        self.order_id = order_id
        self.order_date = order_date
        self.supplier = None
        self.raw_materials = []
        self.payments = []
        self.delivery = None
        self.total_amount = 0.0
        self.status = "pending"  # pending, approved, shipped, delivered, cancelled
        self.expected_delivery = None

    def set_supplier(self, supplier):
        """Установить поставщика"""
        self.supplier = supplier
        supplier.create_purchase_order(self)

    def add_raw_material(self, material, quantity: float, unit_price: float):
        """Добавить сырье"""
        item = {
            'material': material,
            'quantity': quantity,
            'unit_price': unit_price,
            'total': quantity * unit_price
        }
        self.raw_materials.append(item)
        self.total_amount += item['total']

    def add_payment(self, payment):
        """Добавить платеж"""
        self.payments.append(payment)

    def set_delivery(self, delivery):
        """Установить поставку"""
        self.delivery = delivery

    def set_expected_delivery(self, date: datetime):
        """Установить ожидаемую дату доставки"""
        self.expected_delivery = date

    def approve(self):
        """Утвердить заказ"""
        self.status = "approved"
        return {'order': self.order_id, 'approved_at': datetime.now()}

    def mark_shipped(self):
        """Отметить отправленным"""
        self.status = "shipped"
        return {'order': self.order_id, 'shipped_at': datetime.now()}

    def mark_delivered(self):
        """Отметить доставленным"""
        self.status = "delivered"
        return {'order': self.order_id, 'delivered_at': datetime.now()}

    def cancel(self, reason: str):
        """Отменить заказ"""
        self.status = "cancelled"
        return {'order': self.order_id, 'cancelled_at': datetime.now(), 'reason': reason}

    def get_total_quantity(self):
        """Получить общее количество товаров"""
        return sum(item['quantity'] for item in self.raw_materials)

    def is_fully_paid(self):
        """Проверить, полностью ли оплачен"""
        paid_amount = sum(p.get('amount', 0) for p in self.payments)
        return paid_amount >= self.total_amount

    def __repr__(self):
        return f"PurchaseOrder(id='{self.order_id}', amount={self.total_amount}, status='{self.status}')"
