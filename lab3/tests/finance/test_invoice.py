"""Тесты для Invoice"""
import pytest
from factory.finance.invoice import Invoice
from datetime import datetime, timedelta

class TestInvoice:
    def test_creation(self):
        due = datetime.now() + timedelta(days=30)
        inv = Invoice("INV001", 5000.0, due)
        assert inv.invoice_id == "INV001"
        assert inv.amount == 5000.0
        assert inv.status == "unpaid"
    
    def test_mark_paid(self):
        inv = Invoice("INV001", 5000.0, datetime.now())
        inv.mark_paid()
        assert inv.status == "paid"
        assert inv.is_paid() is True
    
    def test_mark_overdue(self):
        inv = Invoice("INV001", 5000.0, datetime.now())
        inv.mark_overdue()
        assert inv.status == "overdue"
