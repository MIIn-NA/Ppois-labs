"""
Склад - место хранения
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Warehouse:
    """Склад"""

    def __init__(self, warehouse_id: str, name: str, capacity: float):
        self.warehouse_id = warehouse_id
        self.name = name
        self.capacity = capacity  # в кубических метрах
        self.factory = None
        self.inventories = []
        self.raw_materials = []
        self.products = []
        self.shipments = []
        self.received_shipments = []
        self.sections = []
        self.current_utilization = 0.0
        self.created_at = datetime.now()
        self.temperature_controlled = False
        self.security_level = "standard"
        self.access_log = []
        self.low_stock_alerts = []

    def assign_to_factory(self, factory):
        """
        Назначить фабрике с регистрацией

        Добавляет склад в систему фабрики
        """
        self.factory = factory
        factory.add_warehouse(self)

        print(f"Warehouse '{self.name}' assigned to factory '{factory.name}'")

        return factory

    def add_inventory(self, inventory):
        """
        Добавить инвентаризацию с валидацией

        Регистрирует проверку запасов
        """
        inventory_record = {
            'inventory': inventory,
            'timestamp': datetime.now(),
            'performed_by': inventory.get('inspector', 'Unknown') if isinstance(inventory, dict) else 'Unknown'
        }

        self.inventories.append(inventory_record)

        print(f"Inventory check added to warehouse '{self.name}'")

        return inventory_record

    def add_raw_material(self, material, quantity: float, unit_volume: float = 1.0):
        """
        Добавить сырье с проверкой емкости

        Валидирует доступное место и обновляет запасы
        """
        if quantity <= 0:
            raise ValueError("Material quantity must be positive")

        # Расчет требуемого объема
        required_volume = quantity * unit_volume

        # Проверка доступной емкости
        available_capacity = self.capacity - self.current_utilization
        if required_volume > available_capacity:
            raise ValueError(
                f"Insufficient warehouse capacity. Required: {required_volume:.2f}m³, Available: {available_capacity:.2f}m³"
            )

        # Проверка на существующий материал
        existing_material = None
        for mat in self.raw_materials:
            if mat['material'] == material:
                existing_material = mat
                break

        if existing_material:
            existing_material['quantity'] += quantity
            existing_material['last_updated'] = datetime.now()
            print(f"Material '{material}' quantity increased: +{quantity} (Total: {existing_material['quantity']})")
        else:
            material_record = {
                'material': material,
                'quantity': quantity,
                'unit_volume': unit_volume,
                'added_at': datetime.now(),
                'last_updated': datetime.now(),
                'min_stock_level': quantity * 0.2  # 20% от начального количества
            }
            self.raw_materials.append(material_record)
            print(f"New material '{material}' added: {quantity} units")

            if hasattr(material, 'add_warehouse'):
                material.add_warehouse(self)

        # Обновление загрузки склада
        self.current_utilization += required_volume

        print(f"Warehouse utilization: {self.get_utilization_percentage():.1f}%")

        return material

    def remove_raw_material(self, material, quantity: float):
        """
        Изъять сырье со склада

        Уменьшает запасы и проверяет критические уровни
        """
        if quantity <= 0:
            raise ValueError("Removal quantity must be positive")

        # Поиск материала
        material_record = None
        for mat in self.raw_materials:
            if mat['material'] == material:
                material_record = mat
                break

        if not material_record:
            raise ValueError(f"Material '{material}' not found in warehouse")

        # Проверка достаточности запасов
        if material_record['quantity'] < quantity:
            raise ValueError(
                f"Insufficient material. Requested: {quantity}, Available: {material_record['quantity']}"
            )

        # Изъятие
        material_record['quantity'] -= quantity
        material_record['last_updated'] = datetime.now()

        # Освобождение объема
        freed_volume = quantity * material_record['unit_volume']
        self.current_utilization = max(0, self.current_utilization - freed_volume)

        # Проверка низкого уровня запасов
        if material_record['quantity'] < material_record['min_stock_level']:
            self._create_low_stock_alert(material, material_record['quantity'], material_record['min_stock_level'])

        print(f"Removed {quantity} units of '{material}'. Remaining: {material_record['quantity']}")

        return material_record

    def _create_low_stock_alert(self, material, current_level: float, min_level: float):
        """Создать предупреждение о низком уровне запасов"""
        alert = {
            'material': material,
            'current_level': current_level,
            'min_level': min_level,
            'severity': 'critical' if current_level < min_level * 0.5 else 'warning',
            'created_at': datetime.now()
        }

        self.low_stock_alerts.append(alert)

        print(f"LOW STOCK ALERT: Material '{material}' below minimum level")
        print(f"Current: {current_level:.2f} | Minimum: {min_level:.2f}")

        return alert

    def add_product(self, product, quantity: int, unit_volume: float = 0.5):
        """
        Добавить готовый продукт с валидацией

        Размещает продукцию на складе
        """
        if quantity <= 0:
            raise ValueError("Product quantity must be positive")

        # Проверка емкости
        required_volume = quantity * unit_volume
        available_capacity = self.capacity - self.current_utilization

        if required_volume > available_capacity:
            raise ValueError(
                f"Insufficient warehouse capacity for products. Required: {required_volume:.2f}m³, Available: {available_capacity:.2f}m³"
            )

        # Поиск существующего продукта
        existing_product = None
        for prod in self.products:
            if prod['product'] == product:
                existing_product = prod
                break

        if existing_product:
            existing_product['quantity'] += quantity
            existing_product['last_updated'] = datetime.now()
            print(f"Product '{product}' quantity increased: +{quantity} (Total: {existing_product['quantity']})")
        else:
            product_record = {
                'product': product,
                'quantity': quantity,
                'unit_volume': unit_volume,
                'added_at': datetime.now(),
                'last_updated': datetime.now(),
                'expiry_date': datetime.now() + timedelta(days=365) if hasattr(product, 'perishable') else None
            }
            self.products.append(product_record)
            print(f"New product '{product}' added: {quantity} units")

        # Обновление загрузки
        self.current_utilization += required_volume

        print(f"Warehouse utilization: {self.get_utilization_percentage():.1f}%")

        return product

    def ship_product(self, product, quantity: int, destination: str):
        """
        Отгрузить продукт покупателю

        Создает отгрузку и уменьшает запасы
        """
        if quantity <= 0:
            raise ValueError("Shipment quantity must be positive")

        # Поиск продукта
        product_record = None
        for prod in self.products:
            if prod['product'] == product:
                product_record = prod
                break

        if not product_record:
            raise ValueError(f"Product '{product}' not found in warehouse")

        if product_record['quantity'] < quantity:
            raise ValueError(
                f"Insufficient product quantity. Requested: {quantity}, Available: {product_record['quantity']}"
            )

        # Создание отгрузки
        shipment = {
            'shipment_id': f"SHIP-{len(self.shipments) + 1:06d}",
            'product': product,
            'quantity': quantity,
            'destination': destination,
            'shipped_at': datetime.now(),
            'status': 'dispatched'
        }

        self.shipments.append(shipment)

        # Уменьшение запасов
        product_record['quantity'] -= quantity
        freed_volume = quantity * product_record['unit_volume']
        self.current_utilization = max(0, self.current_utilization - freed_volume)

        print(f"Shipment created: {shipment['shipment_id']}")
        print(f"Product: {product} | Quantity: {quantity} | Destination: {destination}")
        print(f"Remaining stock: {product_record['quantity']}")

        return shipment

    def receive_shipment(self, items: List[Dict], supplier: str):
        """
        Принять поставку от поставщика

        Регистрирует входящую поставку
        """
        if not items:
            raise ValueError("Shipment must contain at least one item")

        shipment = {
            'shipment_id': f"RCV-{len(self.received_shipments) + 1:06d}",
            'supplier': supplier,
            'items': items,
            'received_at': datetime.now(),
            'status': 'received'
        }

        self.received_shipments.append(shipment)

        # Добавление материалов
        for item in items:
            if 'material' in item:
                self.add_raw_material(
                    item['material'],
                    item.get('quantity', 0),
                    item.get('unit_volume', 1.0)
                )

        print(f"Shipment received: {shipment['shipment_id']} from {supplier}")
        print(f"Items: {len(items)}")

        return shipment

    def create_shipment(self, shipment):
        """Создать отгрузку (устаревший метод, используйте ship_product)"""
        self.shipments.append(shipment)
        print(f"Shipment created via legacy method")
        return shipment

    def add_section(self, section_name: str, section_capacity: float):
        """
        Добавить секцию склада

        Организует склад по зонам
        """
        if section_capacity > self.capacity:
            raise ValueError("Section capacity cannot exceed warehouse capacity")

        section = {
            'section_id': f"SEC-{len(self.sections) + 1:03d}",
            'name': section_name,
            'capacity': section_capacity,
            'utilization': 0.0,
            'created_at': datetime.now()
        }

        self.sections.append(section)

        print(f"Section '{section_name}' added to warehouse '{self.name}'")
        print(f"Capacity: {section_capacity}m³")

        return section

    def log_access(self, person: str, action: str):
        """
        Записать доступ к складу

        Отслеживает безопасность и учет
        """
        access_record = {
            'person': person,
            'action': action,
            'timestamp': datetime.now(),
            'warehouse': self.name
        }

        self.access_log.append(access_record)

        return access_record

    def get_total_inventory_value(self):
        """
        Получить общую стоимость запасов

        Суммирует стоимость всех материалов и продуктов
        """
        total = 0.0

        # Стоимость инвентаризаций
        for inv in self.inventories:
            if isinstance(inv, dict) and 'inventory' in inv:
                inv_obj = inv['inventory']
                if hasattr(inv_obj, 'get_total_value'):
                    total += inv_obj.get_total_value()

        # Можно добавить оценку материалов и продуктов если есть цены

        return round(total, 2)

    def get_utilization_percentage(self):
        """Получить процент заполненности"""
        if self.capacity == 0:
            return 0.0
        return round((self.current_utilization / self.capacity) * 100, 2)

    def is_full(self):
        """Проверить, заполнен ли склад (>95%)"""
        return self.current_utilization >= self.capacity * 0.95

    def get_available_capacity(self) -> float:
        """Получить доступную емкость"""
        return round(max(0, self.capacity - self.current_utilization), 2)

    def get_warehouse_statistics(self) -> Dict:
        """
        Получить полную статистику склада

        Возвращает детальную информацию
        """
        stats = {
            'warehouse_id': self.warehouse_id,
            'warehouse_name': self.name,
            'total_capacity': self.capacity,
            'current_utilization': round(self.current_utilization, 2),
            'available_capacity': self.get_available_capacity(),
            'utilization_percentage': self.get_utilization_percentage(),
            'is_full': self.is_full(),
            'raw_materials_count': len(self.raw_materials),
            'products_count': len(self.products),
            'total_shipments': len(self.shipments),
            'received_shipments': len(self.received_shipments),
            'sections_count': len(self.sections),
            'low_stock_alerts': len(self.low_stock_alerts),
            'inventory_value': self.get_total_inventory_value(),
            'temperature_controlled': self.temperature_controlled,
            'security_level': self.security_level,
            'access_log_entries': len(self.access_log)
        }

        return stats

    def __repr__(self):
        return f"Warehouse(name='{self.name}', utilization={self.get_utilization_percentage():.1f}%, capacity={self.capacity}m³)"
