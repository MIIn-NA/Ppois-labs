"""Тесты для Contract"""
import pytest
from factory.suppliers.contract import Contract
from datetime import datetime, timedelta

class TestContract:
    def test_creation(self):
        start = datetime.now()
        end = start + timedelta(days=365)
        c = Contract("CON001", start, end)
        assert c.contract_id == "CON001"
        assert c.status == "draft"
    
    def test_sign(self):
        c = Contract("CON001", datetime.now(), datetime.now())
        c.sign()
        assert c.status == "active"
    
    def test_is_active(self):
        start = datetime.now()
        end = start + timedelta(days=365)
        c = Contract("CON001", start, end)
        c.sign()
        assert c.is_active() is True
