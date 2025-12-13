"""
Прейскурант - список цен
"""
from datetime import datetime
from typing import List


class PriceList:
    """Прейскурант"""

    def __init__(self, list_id: str, name: str):
        self.list_id = list_id
        self.name = name
        self.prices = []
        self.products = []
        self.customers = []
        self.valid_from = datetime.now()
        self.valid_until = None
        self.is_active = True
        self.created_at = datetime.now()

    def add_price(self, price):
        """Добавить цену"""
        self.prices.append(price)
        price.set_price_list(self)

    def add_product(self, product):
        """Добавить продукт"""
        self.products.append(product)

    def add_customer(self, customer):
        """Добавить клиента"""
        self.customers.append(customer)

    def set_validity_period(self, valid_from: datetime, valid_until: datetime):
        """Установить период действия"""
        self.valid_from = valid_from
        self.valid_until = valid_until

    def activate(self):
        """Активировать прейскурант"""
        self.is_active = True

    def deactivate(self):
        """Деактивировать прейскурант"""
        self.is_active = False

    def get_price_for_product(self, product):
        """Получить цену для продукта"""
        for price in self.prices:
            if price.product == product and price.is_valid():
                return price
        return None

    def get_all_active_prices(self):
        """Получить все активные цены"""
        return [price for price in self.prices if price.is_valid()]

    def is_valid(self):
        """Проверить, действителен ли прейскурант"""
        now = datetime.now()
        if not self.is_active:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return now >= self.valid_from

    def __repr__(self):
        return f"PriceList(name='{self.name}', prices={len(self.prices)})"
