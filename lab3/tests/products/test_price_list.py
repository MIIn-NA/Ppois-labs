"""Тесты для PriceList"""
import pytest
from factory.products.price_list import PriceList

class TestPriceList:
    def test_creation(self):
        pl = PriceList("PL001", "Standard Prices")
        assert pl.list_id == "PL001"
        assert pl.name == "Standard Prices"
        assert pl.is_active is True
    
    def test_activate_deactivate(self):
        pl = PriceList("PL001", "Standard")
        pl.deactivate()
        assert pl.is_active is False
        pl.activate()
        assert pl.is_active is True
