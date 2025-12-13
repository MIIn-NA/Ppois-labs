"""Тесты для StorageLocation"""
import pytest
from factory.warehouse.storage_location import StorageLocation
from factory.products.product import Product

class TestStorageLocation:
    def test_creation(self):
        loc = StorageLocation("LOC001", "A-01-15")
        assert loc.location_id == "LOC001"
        assert loc.code == "A-01-15"
        assert loc.is_occupied is False
    
    def test_store_product(self):
        loc = StorageLocation("LOC001", "A-01-15")
        p = Product("P1", "Widget", "Test")
        loc.store_product(p, 50)
        assert loc.is_occupied is True
        assert loc.quantity == 50
    
    def test_remove_items(self):
        loc = StorageLocation("LOC001", "A-01-15")
        p = Product("P1", "Widget", "Test")
        loc.store_product(p, 50)
        loc.remove_items(20)
        assert loc.quantity == 30
    
    def test_clear(self):
        loc = StorageLocation("LOC001", "A-01-15")
        p = Product("P1", "Widget", "Test")
        loc.store_product(p, 50)
        loc.clear()
        assert loc.is_occupied is False
