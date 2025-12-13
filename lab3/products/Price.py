"""
Цена - ценовая информация
"""
from datetime import datetime


class Price:
    """Цена"""

    def __init__(self, price_id: str, amount: float, currency: str = "USD"):
        self.price_id = price_id
        self.amount = amount
        self.currency = currency
        self.product = None
        self.orders = []
        self.price_list = None
        self.discount = None
        self.valid_from = datetime.now()
        self.valid_until = None
        self.is_active = True

    def set_product(self, product):
        """Установить продукт"""
        self.product = product
        product.set_price(self)

    def add_order(self, order):
        """Добавить заказ"""
        self.orders.append(order)

    def set_price_list(self, price_list):
        """Установить прейскурант"""
        self.price_list = price_list

    def apply_discount(self, discount):
        """Применить скидку"""
        self.discount = discount

    def set_validity_period(self, valid_from: datetime, valid_until: datetime):
        """Установить период действия"""
        self.valid_from = valid_from
        self.valid_until = valid_until

    def update_amount(self, new_amount: float):
        """Обновить цену"""
        self.amount = new_amount

    def deactivate(self):
        """Деактивировать цену"""
        self.is_active = False

    def get_final_price(self):
        """Получить итоговую цену с учетом скидки"""
        if self.discount and hasattr(self.discount, 'percentage'):
            discount_amount = self.amount * (self.discount.percentage / 100)
            return self.amount - discount_amount
        return self.amount

    def is_valid(self):
        """Проверить, действительна ли цена"""
        now = datetime.now()
        if not self.is_active:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return now >= self.valid_from

    def __repr__(self):
        return f"Price(amount={self.amount} {self.currency}, product='{self.product.name if self.product else None}')"
