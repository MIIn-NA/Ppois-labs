"""
График работы - расписание сотрудников
"""
from datetime import datetime, date
from typing import List, Dict


class WorkSchedule:
    """График работы"""

    def __init__(self, schedule_id: str, start_date: date, end_date: date):
        self.schedule_id = schedule_id
        self.start_date = start_date
        self.end_date = end_date
        self.employees = []
        self.shifts = []
        self.department = None
        self.schedule_data = {}  # {employee_id: {date: shift}}

    def add_employee(self, employee):
        """Добавить сотрудника в расписание"""
        self.employees.append(employee)
        employee.set_work_schedule(self)

    def add_shift(self, shift):
        """Добавить смену"""
        self.shifts.append(shift)

    def assign_employee_to_shift(self, employee, shift, work_date: date):
        """Назначить сотрудника на смену"""
        if employee.employee_id not in self.schedule_data:
            self.schedule_data[employee.employee_id] = {}
        self.schedule_data[employee.employee_id][work_date] = shift

    def get_employee_shift(self, employee, work_date: date):
        """Получить смену сотрудника на дату"""
        return self.schedule_data.get(employee.employee_id, {}).get(work_date)

    def get_employees_on_shift(self, shift, work_date: date):
        """Получить сотрудников на смене в определенную дату"""
        employees = []
        for emp_id, dates in self.schedule_data.items():
            if dates.get(work_date) == shift:
                emp = next((e for e in self.employees if e.employee_id == emp_id), None)
                if emp:
                    employees.append(emp)
        return employees

    def set_department(self, department):
        """Установить отдел"""
        self.department = department

    def is_employee_working(self, employee, work_date: date):
        """Проверить, работает ли сотрудник в дату"""
        return work_date in self.schedule_data.get(employee.employee_id, {})

    def __repr__(self):
        return f"WorkSchedule(id='{self.schedule_id}', employees={len(self.employees)})"
