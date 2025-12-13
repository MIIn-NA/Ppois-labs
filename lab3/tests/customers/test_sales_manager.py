"""Тесты для SalesManager"""
import pytest
from factory.customers.sales_manager import SalesManager

import pytest
from datetime import datetime

# Моки для зависимостей
class MockCustomer:
    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active

class MockOrder:
    def __init__(self, order_id, total_amount=None):
        self.order_id = order_id
        if total_amount is not None:
            self.total_amount = total_amount

class MockReport:
    def __init__(self, report_id):
        self.report_id = report_id




class TestSalesManager:
    def test_creation_and_initial_state(self):
        sm = SalesManager("Alice Sales", "SM001", 65000.0)
        assert sm.name == "Alice Sales"
        assert sm.employee_id == "SM001"
        assert sm.salary == 65000.0
        assert sm.department is None
        assert sm.customers == []
        assert sm.orders == []
        assert sm.sales_reports == []
        assert sm.sales_target == 0.0
        assert sm.commission_rate == 0.0
        assert isinstance(sm.hire_date, datetime)
        assert sm.is_active is True
        assert sm.position == "Sales Manager"
        repr_string = repr(sm)
        assert "SalesManager" in repr_string
        assert "customers=0" in repr_string

    def test_add_customer(self):
        sm = SalesManager("Bob", "SM002", 55000)
        c1 = MockCustomer("Customer A")
        c2 = MockCustomer("Customer B", is_active=False)
        sm.add_customer(c1)
        sm.add_customer(c2)
        assert len(sm.customers) == 2
        assert sm.get_active_customers_count() == 1

    def test_create_order_and_total_sales(self):
        sm = SalesManager("Carol", "SM003", 70000)
        o1 = MockOrder("O1", total_amount=10000.0)
        o2 = MockOrder("O2", total_amount=15000.0)
        sm.create_order(o1)
        sm.create_order(o2)
        total = sm.get_total_sales()
        assert total == 25000.0

    def test_get_total_sales_with_missing_total_amount(self):
        sm = SalesManager("Dave", "SM004", 60000)
        o1 = MockOrder("O1")  # нет total_amount
        sm.create_order(o1)
        assert sm.get_total_sales() == 0.0  # не падает при отсутствии атрибута

    def test_submit_sales_report(self):
        sm = SalesManager("Eve", "SM005", 80000)
        report = MockReport("R001")
        returned = sm.submit_sales_report(report)
        assert returned == report
        assert sm.sales_reports == [report]

    def test_set_sales_target(self):
        sm = SalesManager("Fred", "SM006", 90000)
        sm.set_sales_target(120000.0)
        assert sm.sales_target == 120000.0

    def test_set_commission_rate_valid_and_invalid(self):
        sm = SalesManager("Gina", "SM007", 85000)
        sm.set_commission_rate(0.15)
        assert sm.commission_rate == 0.15
        sm.set_commission_rate(-0.1)  # invalid, должно игнорироваться
        assert sm.commission_rate == 0.15
        sm.set_commission_rate(2.0)   # invalid
        assert sm.commission_rate == 0.15

    def test_calculate_commission(self):
        sm = SalesManager("Henry", "SM008", 50000)
        sm.set_commission_rate(0.1)
        sm.create_order(MockOrder("O1", total_amount=20000.0))
        sm.create_order(MockOrder("O2", total_amount=30000.0))
        assert sm.calculate_commission() == 5000.0  # 10% от 50 000

    def test_get_target_achievement(self):
        sm = SalesManager("Ivy", "SM009", 54000)
        sm.set_sales_target(100000.0)
        sm.create_order(MockOrder("O1", total_amount=25000.0))
        result = sm.get_target_achievement()
        assert result == 25.0

    def test_get_target_achievement_with_zero_target(self):
        sm = SalesManager("Jack", "SM010", 62000)
        sm.set_sales_target(0)
        assert sm.get_target_achievement() == 0

    def test_repr_with_customers(self):
        sm = SalesManager("Kate", "SM011", 63000)
        sm.add_customer(MockCustomer("Cust1"))
        repr_str = repr(sm)
        assert "customers=1" in repr_str