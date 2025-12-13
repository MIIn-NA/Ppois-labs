"""
Скидка - скидка для клиента
"""
from datetime import datetime


class Discount:
    """Скидка"""

    def __init__(self, discount_id: str, name: str, percentage: float):
        self.discount_id = discount_id
        self.name = name
        self.percentage = percentage  # 0-100
        self.customers = []
        self.orders = []
        self.price = None
        self.valid_from = datetime.now()
        self.valid_until = None
        self.is_active = True
        self.discount_type = "percentage"  # percentage, fixed_amount

    def add_customer(self, customer):
        """Добавить клиента"""
        self.customers.append(customer)

    def add_order(self, order):
        """Добавить заказ"""
        self.orders.append(order)

    def set_price(self, price):
        """Установить цену"""
        self.price = price
        price.apply_discount(self)

    def set_validity_period(self, valid_from: datetime, valid_until: datetime):
        """Установить период действия"""
        self.valid_from = valid_from
        self.valid_until = valid_until

    def set_discount_type(self, discount_type: str):
        """Установить тип скидки"""
        self.discount_type = discount_type

    def activate(self):
        """Активировать скидку"""
        self.is_active = True

    def deactivate(self):
        """Деактивировать скидку"""
        self.is_active = False

    def is_valid(self):
        """Проверить, действительна ли скидка"""
        now = datetime.now()
        if not self.is_active:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return now >= self.valid_from

    def calculate_discount_amount(self, original_price: float):
        """Рассчитать сумму скидки"""
        if not self.is_valid():
            return 0
        if self.discount_type == "percentage":
            return original_price * (self.percentage / 100)
        else:
            return self.percentage  # фиксированная сумма

    def apply_to_price(self, original_price: float):
        """Применить к цене"""
        discount_amount = self.calculate_discount_amount(original_price)
        return original_price - discount_amount

    def __repr__(self):
        return f"Discount(name='{self.name}', percentage={self.percentage}%)"
