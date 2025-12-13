"""
Директор фабрики - принимает стратегические решения
"""
from typing import List
from datetime import datetime


class Director:
    """Директор фабрики"""

    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id
        self.factory = None
        self.departments = []
        self.production_plans = []
        self.financial_reports = []
        self.hire_date = datetime.now()

    def assign_to_factory(self, factory):
        """Назначить на фабрику"""
        self.factory = factory

    def add_department(self, department):
        """Добавить отдел под управление"""
        self.departments.append(department)

    def create_production_plan(self, production_plan):
        """Создать план производства"""
        self.production_plans.append(production_plan)
        return production_plan

    def review_financial_report(self, report):
        """Проверить финансовый отчет"""
        self.financial_reports.append(report)

    def make_strategic_decision(self, decision: str):
        """Принять стратегическое решение"""
        return {
            'decision': decision,
            'director': self.name,
            'timestamp': datetime.now()
        }

    def get_departments_count(self):
        """Получить количество отделов"""
        return len(self.departments)

    def __repr__(self):
        return f"Director(name='{self.name}', id='{self.employee_id}')"
