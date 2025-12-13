"""Тесты для SalesReport"""
import pytest
from factory.customers.sales_report import SalesReport
from factory.customers.order import Order
from datetime import datetime

class TestSalesReport:
    def test_creation(self):
        sr = SalesReport("SR001", datetime.now(), datetime.now())
        assert sr.report_id == "SR001"
        assert sr.total_revenue == 0.0
    
    def test_add_order(self):
        sr = SalesReport("SR001", datetime.now(), datetime.now())
        o = Order("O1", datetime.now())
        o.total_amount = 1000.0
        sr.add_order(o)
        assert sr.total_revenue == 1000.0
    
    def test_calculate_average_order_value(self):
        sr = SalesReport("SR001", datetime.now(), datetime.now())
        o1 = Order("O1", datetime.now())
        o1.total_amount = 1000.0
        o2 = Order("O2", datetime.now())
        o2.total_amount = 2000.0
        sr.add_order(o1)
        sr.add_order(o2)
        assert sr.calculate_average_order_value() == 1500.0
