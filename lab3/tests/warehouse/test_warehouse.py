"""Тесты для Warehouse"""
import pytest
from factory.warehouse.warehouse import Warehouse

class TestWarehouse:
    def test_creation(self):
        w = Warehouse("WH001", "Main Warehouse", 1000.0)
        assert w.warehouse_id == "WH001"
        assert w.capacity == 1000.0
    
    def test_get_utilization_percentage(self):
        w = Warehouse("WH001", "Main", 1000.0)
        w.current_utilization = 750.0
        assert w.get_utilization_percentage() == 75.0
    
    def test_is_full(self):
        w = Warehouse("WH001", "Main", 1000.0)
        w.current_utilization = 960.0
        assert w.is_full() is True
