"""
Место хранения - конкретная ячейка хранения
"""
from datetime import datetime


class StorageLocation:
    """Место хранения"""

    def __init__(self, location_id: str, code: str):
        self.location_id = location_id
        self.code = code  # например: "A-01-15" (секция-ряд-место)
        self.warehouse_section = None
        self.product = None
        self.raw_material = None
        self.quantity = 0
        self.is_occupied = False
        self.last_updated = datetime.now()

    def assign_to_section(self, section):
        """Назначить секции"""
        self.warehouse_section = section

    def store_product(self, product, quantity: int):
        """Разместить продукт"""
        self.product = product
        self.quantity = quantity
        self.is_occupied = True
        self.last_updated = datetime.now()
        return {'location': self.code, 'product': product, 'quantity': quantity}

    def store_raw_material(self, material, quantity: float):
        """Разместить сырье"""
        self.raw_material = material
        self.quantity = quantity
        self.is_occupied = True
        self.last_updated = datetime.now()
        return {'location': self.code, 'material': material, 'quantity': quantity}

    def remove_items(self, quantity):
        """Удалить товары"""
        if quantity <= self.quantity:
            self.quantity -= quantity
            if self.quantity == 0:
                self.clear()
            else:
                self.last_updated = datetime.now()
            return True
        return False

    def clear(self):
        """Очистить место хранения"""
        self.product = None
        self.raw_material = None
        self.quantity = 0
        self.is_occupied = False
        self.last_updated = datetime.now()

    def get_stored_item(self):
        """Получить хранящийся товар"""
        if self.product:
            return {'type': 'product', 'item': self.product, 'quantity': self.quantity}
        elif self.raw_material:
            return {'type': 'raw_material', 'item': self.raw_material, 'quantity': self.quantity}
        return None

    def __repr__(self):
        status = "occupied" if self.is_occupied else "empty"
        return f"StorageLocation(code='{self.code}', status='{status}')"
