"""
Тесты для класса Manager
"""
import pytest
from factory.management.manager import Manager
from factory.management.department import Department
from factory.personnel.employee import Employee


class TestManager:
    """Тесты для класса Manager"""

    def test_manager_creation(self):
        """Тест создания менеджера"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        assert manager.name == "Alice Brown"
        assert manager.employee_id == "MGR-001"
        assert manager.salary == 70000
        assert manager.department is None
        assert len(manager.employees) == 0

    def test_assign_to_department(self):
        """Тест назначения на отдел"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        dept = Department("HR", "DEPT-001")
        manager.assign_to_department(dept)
        assert manager.department == dept
        assert dept.manager == manager

    def test_add_employee(self):
        """Тест добавления сотрудника"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        emp = Employee("Bob Smith", "EMP-001", 50000)
        manager.add_employee(emp)
        assert len(manager.employees) == 1
        assert emp in manager.employees

    def test_create_task(self):
        """Тест создания задачи"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        task = {"task_id": "TASK-001", "description": "Review reports"}
        result = manager.create_task(task)
        assert result == task
        assert len(manager.tasks) == 1
        assert task in manager.tasks

    def test_submit_report(self):
        """Тест отправки отчета"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        report = {"report_id": "REP-001", "data": "Monthly report"}
        result = manager.submit_report(report)
        assert result == report
        assert len(manager.reports) == 1
        assert report in manager.reports

    def test_get_team_size(self):
        """Тест получения размера команды"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        assert manager.get_team_size() == 0
        manager.add_employee(Employee("Emp1", "EMP-001", 50000))
        manager.add_employee(Employee("Emp2", "EMP-002", 60000))
        assert manager.get_team_size() == 2

    def test_get_completed_tasks(self):
        """Тест получения завершенных задач"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        task1 = {"task_id": "TASK-001", "completed": True}
        task2 = {"task_id": "TASK-002", "completed": False}
        task3 = {"task_id": "TASK-003", "completed": True}
        manager.create_task(task1)
        manager.create_task(task2)
        manager.create_task(task3)
        completed = manager.get_completed_tasks()
        assert len(completed) == 2
        assert task1 in completed
        assert task3 in completed
        assert task2 not in completed

    def test_repr(self):
        """Тест строкового представления"""
        manager = Manager("Alice Brown", "MGR-001", 70000)
        dept = Department("HR", "DEPT-001")
        manager.assign_to_department(dept)
        assert "Alice Brown" in repr(manager)
        assert "HR" in repr(manager)
