"""Тесты для Product"""
import pytest
from factory.products.product import Product

class TestProduct:
    def test_creation(self):
        p = Product("P001", "Widget", "Test product")
        assert p.product_id == "P001"
        assert p.name == "Widget"
        assert p.is_active is True
    
    def test_discontinue(self):
        p = Product("P001", "Widget", "Test")
        p.discontinue()
        assert p.is_active is False
    
    def test_get_total_produced(self):
        from factory.production.batch import Batch
        p = Product("P001", "Widget", "Test")
        b1 = Batch("B1", 100)
        b2 = Batch("B2", 150)
        p.add_batch(b1)
        p.add_batch(b2)
        assert p.get_total_produced() == 250
