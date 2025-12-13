"""Тесты для Discount"""
import pytest
from factory.customers.discount import Discount

class TestDiscount:
    def test_creation(self):
        d = Discount("DIS001", "Summer Sale", 20.0)
        assert d.discount_id == "DIS001"
        assert d.percentage == 20.0
        assert d.is_active is True
    
    def test_calculate_discount_amount(self):
        d = Discount("DIS001", "Sale", 20.0)
        amount = d.calculate_discount_amount(100.0)
        assert amount == 20.0
    
    def test_apply_to_price(self):
        d = Discount("DIS001", "Sale", 15.0)
        final = d.apply_to_price(200.0)
        assert final == 170.0
