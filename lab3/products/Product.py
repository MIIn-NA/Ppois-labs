"""
Готовая продукция - конечный продукт фабрики
"""
from datetime import datetime
from typing import List


class Product:
    """Готовая продукция"""

    def __init__(self, product_id: str, name: str, description: str):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.production_lines = []
        self.batches = []
        self.orders = []
        self.price = None
        self.specification = None
        self.category = ""
        self.is_active = True
        self.created_at = datetime.now()

    def add_to_production_line(self, production_line):
        """Добавить на производственную линию"""
        self.production_lines.append(production_line)
        production_line.add_product(self)

    def add_batch(self, batch):
        """Добавить партию"""
        self.batches.append(batch)

    def add_order(self, order):
        """Добавить заказ"""
        self.orders.append(order)

    def set_price(self, price):
        """Установить цену"""
        self.price = price

    def set_specification(self, specification):
        """Установить спецификацию"""
        self.specification = specification

    def set_category(self, category: str):
        """Установить категорию"""
        self.category = category

    def discontinue(self):
        """Снять с производства"""
        self.is_active = False

    def get_total_produced(self):
        """Получить общее произведенное количество"""
        return sum(batch.quantity for batch in self.batches)

    def get_current_price(self):
        """Получить текущую цену"""
        if self.price:
            return self.price.amount if hasattr(self.price, 'amount') else 0
        return 0

    def __repr__(self):
        return f"Product(id='{self.product_id}', name='{self.name}')"
