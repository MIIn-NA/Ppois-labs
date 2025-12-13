"""
Сырье - исходные материалы
"""
from datetime import datetime
from typing import List


class RawMaterial:
    """Сырье"""

    def __init__(self, material_id: str, name: str, unit_price: float):
        self.material_id = material_id
        self.name = name
        self.unit_price = unit_price
        self.supplier = None
        self.warehouses = []
        self.production_orders = []
        self.material_requests = []
        self.unit_of_measure = "kg"  # kg, pcs, liters, etc.
        self.current_stock = 0
        self.minimum_stock = 100
        self.created_at = datetime.now()

    def set_supplier(self, supplier):
        """Установить поставщика"""
        self.supplier = supplier

    def add_warehouse(self, warehouse):
        """Добавить склад"""
        self.warehouses.append(warehouse)

    def add_to_production_order(self, production_order):
        """Добавить к производственному заказу"""
        self.production_orders.append(production_order)

    def create_material_request(self, request):
        """Создать заявку на материал"""
        self.material_requests.append(request)
        return request

    def set_unit_of_measure(self, unit: str):
        """Установить единицу измерения"""
        self.unit_of_measure = unit

    def add_stock(self, quantity: float):
        """Добавить к запасу"""
        self.current_stock += quantity

    def reduce_stock(self, quantity: float):
        """Уменьшить запас"""
        if self.current_stock >= quantity:
            self.current_stock -= quantity
            return True
        return False

    def is_low_stock(self):
        """Проверить, мало ли запасов"""
        return self.current_stock < self.minimum_stock

    def set_minimum_stock(self, quantity: float):
        """Установить минимальный запас"""
        self.minimum_stock = quantity

    def calculate_total_value(self):
        """Рассчитать общую стоимость запасов"""
        return self.current_stock * self.unit_price

    def __repr__(self):
        return f"RawMaterial(name='{self.name}', stock={self.current_stock} {self.unit_of_measure})"
