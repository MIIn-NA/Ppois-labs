"""
Спецификация продукта - техническое описание продукта
"""
from typing import List, Dict
from datetime import datetime


class ProductSpecification:
    """Спецификация продукта"""

    def __init__(self, spec_id: str, version: str):
        self.spec_id = spec_id
        self.version = version
        self.product = None
        self.raw_materials = []
        self.technical_documentation = []
        self.specifications = {}  # технические характеристики
        self.requirements = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def set_product(self, product):
        """Установить продукт"""
        self.product = product
        product.set_specification(self)

    def add_raw_material(self, material, quantity: float):
        """Добавить сырье"""
        self.raw_materials.append({
            'material': material,
            'quantity': quantity
        })

    def add_technical_documentation(self, doc):
        """Добавить техническую документацию"""
        self.technical_documentation.append(doc)

    def add_specification(self, key: str, value):
        """Добавить техническую характеристику"""
        self.specifications[key] = value
        self.updated_at = datetime.now()

    def add_requirement(self, requirement: str):
        """Добавить требование"""
        self.requirements.append(requirement)

    def update_version(self, new_version: str):
        """Обновить версию"""
        self.version = new_version
        self.updated_at = datetime.now()

    def get_material_list(self):
        """Получить список материалов"""
        return [rm['material'] for rm in self.raw_materials]

    def get_total_material_cost(self):
        """Получить общую стоимость материалов"""
        total = 0
        for rm in self.raw_materials:
            material = rm['material']
            quantity = rm['quantity']
            if hasattr(material, 'unit_price'):
                total += material.unit_price * quantity
        return total

    def __repr__(self):
        return f"ProductSpecification(id='{self.spec_id}', version='{self.version}')"
