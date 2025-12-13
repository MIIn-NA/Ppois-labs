"""Тесты для Supplier"""
import pytest
from factory.suppliers.supplier import Supplier

class TestSupplier:
    def test_creation(self):
        s = Supplier("SUP001", "ABC Supplies", "contact@abc.com")
        assert s.supplier_id == "SUP001"
        assert s.name == "ABC Supplies"
        assert s.is_active is True
    
    def test_update_rating(self):
        s = Supplier("SUP001", "ABC Supplies", "contact@abc.com")
        s.update_rating(4.5)
        assert s.rating == 4.5
    
    def test_deactivate(self):
        s = Supplier("SUP001", "ABC Supplies", "contact@abc.com")
        s.deactivate()
        assert s.is_active is False
