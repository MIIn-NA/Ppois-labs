"""Тесты для Order"""
import pytest
from factory.customers.order import Order
from factory.products.product import Product
from datetime import datetime

class TestOrder:
    def test_creation(self):
        o = Order("ORD001", datetime.now())
        assert o.order_id == "ORD001"
        assert o.status == "pending"
    
    def test_add_product(self):
        o = Order("ORD001", datetime.now())
        p = Product("P1", "Widget", "Test")
        o.add_product(p, 10, 99.99)
        assert o.total_amount == 999.9
    
    def test_workflow(self):
        o = Order("ORD001", datetime.now())
        o.confirm()
        assert o.status == "confirmed"
        o.start_production()
        assert o.status == "in_production"
        o.mark_shipped()
        assert o.status == "shipped"
        o.mark_delivered()
        assert o.status == "delivered"
