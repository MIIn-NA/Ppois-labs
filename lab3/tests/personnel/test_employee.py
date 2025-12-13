"""
Тесты для класса Employee
"""
import pytest
from factory.personnel.employee import Employee
from factory.management.department import Department
from factory.personnel.shift import Shift
from datetime import time


class TestEmployee:
    """Тесты для класса Employee"""

    def test_employee_creation(self):
        """Тест создания сотрудника"""
        emp = Employee("John Doe", "EMP-001", 50000)
        assert emp.name == "John Doe"
        assert emp.employee_id == "EMP-001"
        assert emp.salary == 50000
        assert emp.is_active is True
        assert emp.position == "Employee"

    def test_assign_to_department(self):
        """Тест назначения в отдел"""
        emp = Employee("John Doe", "EMP-001", 50000)
        dept = Department("HR", "DEPT-001")
        emp.assign_to_department(dept)
        assert emp.department == dept
        assert emp in dept.employees

    def test_assign_shift(self):
        """Тест назначения смены"""
        emp = Employee("John Doe", "EMP-001", 50000)
        shift = Shift("SHIFT-001", "Morning", time(8, 0), time(16, 0))
        emp.assign_shift(shift)
        assert emp.shift == shift

    def test_increase_salary(self):
        """Тест увеличения зарплаты"""
        emp = Employee("John Doe", "EMP-001", 50000)
        emp.increase_salary(5000)
        assert emp.salary == 55000

    def test_terminate(self):
        """Тест увольнения"""
        emp = Employee("John Doe", "EMP-001", 50000)
        emp.terminate()
        assert emp.is_active is False

    def test_get_years_of_service(self):
        """Тест получения стажа"""
        emp = Employee("John Doe", "EMP-001", 50000)
        years = emp.get_years_of_service()
        assert years >= 0

    def test_repr(self):
        """Тест строкового представления"""
        emp = Employee("John Doe", "EMP-001", 50000)
        assert "John Doe" in repr(emp)
        assert "EMP-001" in repr(emp)
