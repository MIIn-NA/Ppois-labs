"""
Заказ от клиента - заказ на продукцию
"""
from datetime import datetime
from typing import List


class Order:
    """Заказ от клиента"""

    def __init__(self, order_id: str, order_date: datetime):
        self.order_id = order_id
        self.order_date = order_date
        self.customer = None
        self.products = []
        self.payments = []
        self.shipment = None
        self.production_order = None
        self.total_amount = 0.0
        self.status = "pending"  # pending, confirmed, in_production, shipped, delivered, cancelled
        self.expected_delivery = None

    def set_customer(self, customer):
        """Установить клиента"""
        self.customer = customer
        customer.create_order(self)

    def add_product(self, product, quantity: int, unit_price: float):
        """Добавить продукт"""
        item = {
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'total': quantity * unit_price
        }
        self.products.append(item)
        self.total_amount += item['total']
        product.add_order(self)

    def add_payment(self, payment):
        """Добавить платеж"""
        self.payments.append(payment)

    def set_shipment(self, shipment):
        """Установить отгрузку"""
        self.shipment = shipment
        shipment.set_order(self)

    def link_production_order(self, production_order):
        """Связать с производственным заказом"""
        self.production_order = production_order
        production_order.link_customer_order(self)

    def set_expected_delivery(self, date: datetime):
        """Установить ожидаемую дату доставки"""
        self.expected_delivery = date

    def confirm(self):
        """Подтвердить заказ"""
        self.status = "confirmed"
        if self.customer:
            self.customer.increase_balance(self.total_amount)
        return {'order': self.order_id, 'confirmed_at': datetime.now()}

    def start_production(self):
        """Начать производство"""
        self.status = "in_production"
        return {'order': self.order_id, 'production_started_at': datetime.now()}

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

    def is_fully_paid(self):
        """Проверить, полностью ли оплачен"""
        paid_amount = sum(p.get('amount', 0) for p in self.payments)
        return paid_amount >= self.total_amount

    def get_total_items(self):
        """Получить общее количество товаров"""
        return sum(p['quantity'] for p in self.products)

    def __repr__(self):
        return f"Order(id='{self.order_id}', amount={self.total_amount}, status='{self.status}')"
