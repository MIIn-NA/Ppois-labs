"""Тесты для класса Accountant"""
import pytest
from factory.personnel.accountant import Accountant
from factory.finance.finance_department import FinanceDepartment
from datetime import datetime


class TestAccountant:
    def test_creation(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        assert acc.name == "Mary Counter"
        assert acc.position == "Accountant"

    def test_assign_to_finance_department(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        fin_dept = FinanceDepartment("FIN-001", "Finance")
        acc.assign_to_finance_department(fin_dept)
        assert acc.finance_department == fin_dept

    def test_create_invoice(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        order = {"order_id": "ORD-001"}
        invoice = acc.create_invoice(order, 10000)
        assert invoice['amount'] == 10000
        assert invoice['status'] == 'pending'
        assert invoice in acc.invoices

    def test_process_payment(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        payment = {"payment_id": "PAY-001", "amount": 5000}
        result = acc.process_payment(payment)
        assert result['status'] == 'processed'
        assert payment in acc.payments

    def test_generate_financial_report(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        report = acc.generate_financial_report("Q1 2024")
        assert report['period'] == "Q1 2024"
        assert 'generated_at' in report

    def test_reconcile_accounts(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        result = acc.reconcile_accounts()
        assert result['status'] == 'balanced'

    def test_get_total_processed_amount(self):
        acc = Accountant("Mary Counter", "ACC-001", 60000)
        acc.process_payment({"amount": 1000})
        acc.process_payment({"amount": 2000})
        assert acc.get_total_processed_amount() == 3000
