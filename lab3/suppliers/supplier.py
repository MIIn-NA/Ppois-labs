"""
Поставщик - поставщик сырья и материалов
"""
from datetime import datetime
from typing import List


class Supplier:
    """Поставщик"""

    def __init__(self, supplier_id: str, name: str, contact_info: str):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info
        self.raw_materials = []
        self.purchase_orders = []
        self.contracts = []
        self.payments = []
        self.rating = 0.0
        self.is_active = True
        self.created_at = datetime.now()

    def add_raw_material(self, material):
        """Добавить сырье"""
        self.raw_materials.append(material)
        material.set_supplier(self)

    def create_purchase_order(self, purchase_order):
        """Создать заказ на закупку"""
        self.purchase_orders.append(purchase_order)
        return purchase_order

    def add_contract(self, contract):
        """Добавить договор"""
        self.contracts.append(contract)

    def add_payment(self, payment):
        """Добавить платеж"""
        self.payments.append(payment)

    def update_rating(self, new_rating: float):
        """Обновить рейтинг"""
        if 0 <= new_rating <= 5:
            self.rating = new_rating

    def get_active_contracts(self):
        """Получить активные договоры"""
        return [c for c in self.contracts if hasattr(c, 'is_active') and c.is_active]

    def get_total_orders_value(self):
        """Получить общую стоимость заказов"""
        total = 0
        for order in self.purchase_orders:
            if hasattr(order, 'total_amount'):
                total += order.total_amount
        return total

    def deactivate(self):
        """Деактивировать поставщика"""
        self.is_active = False

    def activate(self):
        """Активировать поставщика"""
        self.is_active = True

    def __repr__(self):
        return f"Supplier(name='{self.name}', rating={self.rating})"
