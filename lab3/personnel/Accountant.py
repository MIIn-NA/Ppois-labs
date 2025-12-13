"""
Бухгалтер - ведет финансовый учет
"""
from datetime import datetime
from typing import List


class Accountant:
    """Бухгалтер"""

    def __init__(self, name: str, employee_id: str, salary: float):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.department = None
        self.finance_department = None
        self.invoices = []
        self.payments = []
        self.hire_date = datetime.now()
        self.is_active = True
        self.position = "Accountant"

    def assign_to_finance_department(self, finance_dept):
        """Назначить в финансовый отдел"""
        self.finance_department = finance_dept

    def create_invoice(self, order, amount: float):
        """Создать счет"""
        invoice = {
            'order': order,
            'amount': amount,
            'accountant': self.name,
            'created_at': datetime.now(),
            'status': 'pending'
        }
        self.invoices.append(invoice)
        return invoice

    def process_payment(self, payment):
        """Обработать платеж"""
        self.payments.append(payment)
        return {
            'payment': payment,
            'processed_by': self.name,
            'timestamp': datetime.now(),
            'status': 'processed'
        }

    def generate_financial_report(self, period: str):
        """Сгенерировать финансовый отчет"""
        return {
            'period': period,
            'total_invoices': len(self.invoices),
            'total_payments': len(self.payments),
            'accountant': self.name,
            'generated_at': datetime.now()
        }

    def reconcile_accounts(self):
        """Свести счета"""
        return {
            'accountant': self.name,
            'reconciled_at': datetime.now(),
            'status': 'balanced'
        }

    def get_total_processed_amount(self):
        """Получить общую сумму обработанных платежей"""
        return sum(p.get('amount', 0) for p in self.payments)

    def __repr__(self):
        return f"Accountant(name='{self.name}', invoices={len(self.invoices)})"
