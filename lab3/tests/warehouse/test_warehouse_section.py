"""Тесты для WarehouseSection"""
import pytest
from factory.warehouse.warehouse_section import WarehouseSection

class TestWarehouseSection:
    def test_creation(self):
        s = WarehouseSection("SEC001", "Section A", "products")
        assert s.section_id == "SEC001"
        assert s.name == "Section A"
        assert s.section_type == "products"
    
    def test_is_full(self):
        s = WarehouseSection("SEC001", "Section A", "products")
        s.capacity = 2
        from factory.warehouse.storage_location import StorageLocation
        loc1 = StorageLocation("L1", "A-01")
        loc2 = StorageLocation("L2", "A-02")
        loc1.is_occupied = True
        loc2.is_occupied = True
        s.add_storage_location(loc1)
        s.add_storage_location(loc2)
        assert s.is_full() is True
