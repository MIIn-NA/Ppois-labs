"""Тесты для Expense"""
import pytest
from factory.finance.expense import Expense

class TestExpense:
    def test_creation(self):
        e = Expense("EXP001", 5000.0, "salaries", "Monthly salaries")
        assert e.expense_id == "EXP001"
        assert e.amount == 5000.0
        assert e.status == "pending"
    
    def test_approve(self):
        e = Expense("EXP001", 5000.0, "salaries", "Monthly")
        e.approve("Manager")
        assert e.status == "approved"
        assert e.is_approved() is True
    
    def test_reject(self):
        e = Expense("EXP001", 5000.0, "salaries", "Monthly")
        e.reject("Budget exceeded")
        assert e.status == "rejected"
