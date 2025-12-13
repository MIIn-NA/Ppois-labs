"""Тесты для RawMaterial"""
import pytest
from factory.products.raw_material import RawMaterial

class TestRawMaterial:
    def test_creation(self):
        m = RawMaterial("M001", "Steel", 10.5)
        assert m.material_id == "M001"
        assert m.name == "Steel"
        assert m.unit_price == 10.5
    
    def test_add_reduce_stock(self):
        m = RawMaterial("M001", "Steel", 10.5)
        m.add_stock(100)
        assert m.current_stock == 100
        m.reduce_stock(30)
        assert m.current_stock == 70
    
    def test_is_low_stock(self):
        m = RawMaterial("M001", "Steel", 10.5)
        m.set_minimum_stock(50)
        m.add_stock(40)
        assert m.is_low_stock() is True
