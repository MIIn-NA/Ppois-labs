"""
Компонент/деталь - промежуточная деталь
"""
from datetime import datetime
from typing import List


class Component:
    """Компонент/деталь"""

    def __init__(self, component_id: str, name: str):
        self.component_id = component_id
        self.name = name
        self.products = []  # продукты, в которых используется
        self.raw_materials = []  # материалы для изготовления
        self.production_lines = []
        self.inventory = None
        self.unit_cost = 0.0
        self.current_stock = 0
        self.created_at = datetime.now()

    def add_to_product(self, product):
        """Добавить к продукту"""
        self.products.append(product)

    def add_raw_material(self, material, quantity: float):
        """Добавить необходимое сырье"""
        self.raw_materials.append({
            'material': material,
            'quantity': quantity
        })

    def add_production_line(self, production_line):
        """Добавить производственную линию"""
        self.production_lines.append(production_line)

    def set_inventory(self, inventory):
        """Установить инвентаризацию"""
        self.inventory = inventory

    def set_unit_cost(self, cost: float):
        """Установить стоимость единицы"""
        self.unit_cost = cost

    def add_stock(self, quantity: int):
        """Добавить к запасу"""
        self.current_stock += quantity

    def reduce_stock(self, quantity: int):
        """Уменьшить запас"""
        if self.current_stock >= quantity:
            self.current_stock -= quantity
            return True
        return False

    def calculate_production_cost(self):
        """Рассчитать стоимость производства"""
        total = 0
        for rm in self.raw_materials:
            material = rm['material']
            quantity = rm['quantity']
            if hasattr(material, 'unit_price'):
                total += material.unit_price * quantity
        return total

    def get_stock_value(self):
        """Получить стоимость запасов"""
        return self.current_stock * self.unit_cost

    def __repr__(self):
        return f"Component(name='{self.name}', stock={self.current_stock})"
