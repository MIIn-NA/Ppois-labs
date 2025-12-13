"""
Отдел/департамент - организационная единица
"""
from typing import List, Optional
from datetime import datetime


class Department:
    """Отдел/департамент"""

    def __init__(self, name: str, department_id: str):
        self.name = name
        self.department_id = department_id
        self.manager = None
        self.employees = []
        self.budget = None
        self.created_at = datetime.now()

    def set_manager(self, manager):
        """Назначить менеджера отдела"""
        self.manager = manager

    def add_employee(self, employee):
        """Добавить сотрудника"""
        self.employees.append(employee)

    def remove_employee(self, employee):
        """Удалить сотрудника"""
        if employee in self.employees:
            self.employees.remove(employee)

    def set_budget(self, budget):
        """Установить бюджет"""
        self.budget = budget

    def get_employee_count(self):
        """Получить количество сотрудников"""
        return len(self.employees)

    def get_total_salary(self):
        """Получить общий фонд зарплаты"""
        return sum(emp.salary for emp in self.employees if hasattr(emp, 'salary'))

    def __repr__(self):
        return f"Department(name='{self.name}', employees={len(self.employees)})"
