"""
Менеджер по продажам - ведет клиентов
"""
from datetime import datetime
from typing import List


class SalesManager:
    """Менеджер по продажам"""

    def __init__(self, name: str, employee_id: str, salary: float):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.department = None
        self.customers = []
        self.orders = []
        self.sales_reports = []
        self.sales_target = 0.0
        self.commission_rate = 0.0
        self.hire_date = datetime.now()
        self.is_active = True
        self.position = "Sales Manager"

    def add_customer(self, customer):
        """Добавить клиента"""
        self.customers.append(customer)

    def create_order(self, order):
        """Создать заказ"""
        self.orders.append(order)
        return order

    def submit_sales_report(self, report):
        """Отправить отчет о продажах"""
        self.sales_reports.append(report)
        return report

    def set_sales_target(self, target: float):
        """Установить план продаж"""
        self.sales_target = target

    def set_commission_rate(self, rate: float):
        """Установить ставку комиссии"""
        if 0 <= rate <= 1:
            self.commission_rate = rate

    def get_total_sales(self):
        """Получить общий объем продаж"""
        total = 0
        for order in self.orders:
            if hasattr(order, 'total_amount'):
                total += order.total_amount
        return total

    def calculate_commission(self):
        """Рассчитать комиссию"""
        return self.get_total_sales() * self.commission_rate

    def get_target_achievement(self):
        """Получить процент выполнения плана"""
        if self.sales_target == 0:
            return 0
        return (self.get_total_sales() / self.sales_target) * 100

    def get_active_customers_count(self):
        """Получить количество активных клиентов"""
        return len([c for c in self.customers if hasattr(c, 'is_active') and c.is_active])

    def __repr__(self):
        return f"SalesManager(name='{self.name}', customers={len(self.customers)})"
