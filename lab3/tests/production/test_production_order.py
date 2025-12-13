"""Тесты для ProductionOrder"""
import pytest
from factory.production.production_order import ProductionOrder

class TestProductionOrder:
    def test_creation(self):
        po = ProductionOrder("PO001", 100)
        assert po.order_id == "PO001"
        assert po.quantity == 100
        assert po.status == "pending"
    
    def test_start_and_complete(self):
        po = ProductionOrder("PO001", 100)
        po.start_production()
        assert po.status == "in_progress"
        po.complete_production()
        assert po.status == "completed"
    
    def test_get_completion_percentage(self):
        po = ProductionOrder("PO001", 100)
        po.update_produced_quantity(75)
        assert po.get_completion_percentage() == 75.0
