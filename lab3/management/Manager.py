"""
Менеджер отдела - управляет подразделением
"""
from typing import List
from datetime import datetime


class Manager:
    """Менеджер отдела"""

    def __init__(self, name: str, employee_id: str, salary: float):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.department = None
        self.employees = []
        self.tasks = []
        self.reports = []
        self.hire_date = datetime.now()

    def assign_to_department(self, department):
        """Назначить на отдел"""
        self.department = department
        department.set_manager(self)

    def add_employee(self, employee):
        """Добавить сотрудника под управление"""
        self.employees.append(employee)

    def create_task(self, task):
        """Создать задачу"""
        self.tasks.append(task)
        return task

    def submit_report(self, report):
        """Отправить отчет"""
        self.reports.append(report)
        return report

    def get_team_size(self):
        """Получить размер команды"""
        return len(self.employees)

    def get_completed_tasks(self):
        """Получить завершенные задачи"""
        return [task for task in self.tasks if (hasattr(task, 'completed') and task.completed) or (isinstance(task, dict) and task.get('completed'))]

    def __repr__(self):
        return f"Manager(name='{self.name}', department='{self.department.name if self.department else None}')"
