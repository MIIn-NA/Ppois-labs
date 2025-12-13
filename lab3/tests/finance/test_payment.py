"""Тесты для Payment"""
import pytest
from factory.finance.payment import Payment

class TestPayment:
    def test_creation(self):
        p = Payment("PAY001", 1000.0, "incoming")
        assert p.payment_id == "PAY001"
        assert p.amount == 1000.0
        assert p.status == "pending"
    
    def test_complete(self):
        p = Payment("PAY001", 1000.0, "incoming")
        p.complete()
        assert p.status == "completed"
        assert p.is_completed() is True
    
    def test_fail(self):
        p = Payment("PAY001", 1000.0, "incoming")
        p.fail("Insufficient funds")
        assert p.status == "failed"
