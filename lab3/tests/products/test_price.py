"""Тесты для Price"""
import pytest
from factory.products.price import Price

class TestPrice:
    def test_creation(self):
        p = Price("PR001", 99.99, "USD")
        assert p.price_id == "PR001"
        assert p.amount == 99.99
        assert p.is_active is True
    
    def test_update_amount(self):
        p = Price("PR001", 99.99)
        p.update_amount(109.99)
        assert p.amount == 109.99
    
    def test_get_final_price(self):
        p = Price("PR001", 100.0)
        assert p.get_final_price() == 100.0
