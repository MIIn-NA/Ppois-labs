"""
Покупатель/клиент - заказчик продукции
"""
from datetime import datetime
from typing import List


class Customer:
    """Покупатель/клиент"""

    def __init__(self, customer_id: str, name: str, contact_info: str):
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info
        self.orders = []
        self.contracts = []
        self.payments = []
        self.price_list = None
        self.customer_type = "regular"  # regular, vip, wholesale
        self.credit_limit = 0.0
        self.current_balance = 0.0
        self.created_at = datetime.now()
        self.is_active = True

    def create_order(self, order):
        """Создать заказ"""
        self.orders.append(order)
        return order

    def add_contract(self, contract):
        """Добавить договор"""
        self.contracts.append(contract)
        contract.set_customer(self)

    def add_payment(self, payment):
        """Добавить платеж"""
        self.payments.append(payment)
        self.current_balance -= payment.get('amount', 0)

    def set_price_list(self, price_list):
        """Установить прейскурант"""
        self.price_list = price_list
        price_list.add_customer(self)

    def set_customer_type(self, customer_type: str):
        """Установить тип клиента"""
        self.customer_type = customer_type

    def set_credit_limit(self, limit: float):
        """Установить кредитный лимит"""
        self.credit_limit = limit

    def increase_balance(self, amount: float):
        """Увеличить баланс (задолженность)"""
        self.current_balance += amount

    def get_total_orders_value(self):
        """Получить общую стоимость заказов"""
        total = 0
        for order in self.orders:
            if hasattr(order, 'total_amount'):
                total += order.total_amount
        return total

    def can_place_order(self, order_amount: float):
        """Проверить, может ли разместить заказ"""
        potential_balance = self.current_balance + order_amount
        return potential_balance <= self.credit_limit

    def deactivate(self):
        """Деактивировать клиента"""
        self.is_active = False

    def __repr__(self):
        return f"Customer(name='{self.name}', type='{self.customer_type}')"
