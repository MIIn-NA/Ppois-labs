"""
Тесты для класса Department
"""
import pytest
from factory.management.department import Department
from factory.management.manager import Manager
from factory.personnel.employee import Employee


class TestDepartment:
    """Тесты для класса Department"""

    def test_department_creation(self):
        """Тест создания отдела"""
        dept = Department("HR Department", "DEPT-001")
        assert dept.name == "HR Department"
        assert dept.department_id == "DEPT-001"
        assert dept.manager is None
        assert len(dept.employees) == 0

    def test_set_manager(self):
        """Тест назначения менеджера"""
        dept = Department("HR", "DEPT-001")
        manager = Manager("Alice Brown", "MGR-001", 70000)
        dept.set_manager(manager)
        assert dept.manager == manager

    def test_add_employee(self):
        """Тест добавления сотрудника"""
        dept = Department("HR", "DEPT-001")
        emp = Employee("Bob Smith", "EMP-001", 50000)
        dept.add_employee(emp)
        assert len(dept.employees) == 1
        assert emp in dept.employees

    def test_remove_employee(self):
        """Тест удаления сотрудника"""
        dept = Department("HR", "DEPT-001")
        emp = Employee("Bob Smith", "EMP-001", 50000)
        dept.add_employee(emp)
        dept.remove_employee(emp)
        assert len(dept.employees) == 0
        assert emp not in dept.employees

    def test_remove_nonexistent_employee(self):
        """Тест удаления несуществующего сотрудника"""
        dept = Department("HR", "DEPT-001")
        emp = Employee("Bob Smith", "EMP-001", 50000)
        dept.remove_employee(emp)  # Не должно вызывать ошибку
        assert len(dept.employees) == 0

    def test_set_budget(self):
        """Тест установки бюджета"""
        from factory.finance.budget import Budget
        from datetime import datetime
        dept = Department("HR", "DEPT-001")
        budget = Budget("BUD-001", datetime.now(), datetime.now(), 100000)
        dept.set_budget(budget)
        assert dept.budget == budget

    def test_get_employee_count(self):
        """Тест получения количества сотрудников"""
        dept = Department("HR", "DEPT-001")
        assert dept.get_employee_count() == 0
        dept.add_employee(Employee("Emp1", "EMP-001", 50000))
        dept.add_employee(Employee("Emp2", "EMP-002", 60000))
        assert dept.get_employee_count() == 2

    def test_get_total_salary(self):
        """Тест получения общего фонда зарплаты"""
        dept = Department("HR", "DEPT-001")
        dept.add_employee(Employee("Emp1", "EMP-001", 50000))
        dept.add_employee(Employee("Emp2", "EMP-002", 60000))
        assert dept.get_total_salary() == 110000

    def test_repr(self):
        """Тест строкового представления"""
        dept = Department("HR Department", "DEPT-001")
        assert "HR Department" in repr(dept)
        assert "employees=0" in repr(dept)
