"""Тесты для класса WorkSchedule"""
import pytest
from factory.personnel.work_schedule import WorkSchedule
from factory.personnel.employee import Employee
from factory.personnel.shift import Shift
from datetime import date, time


class TestWorkSchedule:
    def test_creation(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 31)
        schedule = WorkSchedule("SCH-001", start, end)
        assert schedule.schedule_id == "SCH-001"
        assert schedule.start_date == start
        assert schedule.end_date == end

    def test_add_employee(self):
        schedule = WorkSchedule("SCH-001", date.today(), date.today())
        emp = Employee("John", "E001", 50000)
        schedule.add_employee(emp)
        assert emp in schedule.employees
        assert emp.work_schedule == schedule

    def test_add_shift(self):
        schedule = WorkSchedule("SCH-001", date.today(), date.today())
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        schedule.add_shift(shift)
        assert shift in schedule.shifts

    def test_assign_employee_to_shift(self):
        schedule = WorkSchedule("SCH-001", date.today(), date.today())
        emp = Employee("John", "E001", 50000)
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        work_date = date(2024, 1, 15)
        schedule.assign_employee_to_shift(emp, shift, work_date)
        assert schedule.get_employee_shift(emp, work_date) == shift

    def test_get_employees_on_shift(self):
        schedule = WorkSchedule("SCH-001", date.today(), date.today())
        emp1 = Employee("John", "E001", 50000)
        emp2 = Employee("Jane", "E002", 50000)
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        schedule.add_employee(emp1)
        schedule.add_employee(emp2)
        work_date = date(2024, 1, 15)
        schedule.assign_employee_to_shift(emp1, shift, work_date)
        schedule.assign_employee_to_shift(emp2, shift, work_date)
        employees = schedule.get_employees_on_shift(shift, work_date)
        assert len(employees) == 2

    def test_is_employee_working(self):
        schedule = WorkSchedule("SCH-001", date.today(), date.today())
        emp = Employee("John", "E001", 50000)
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        work_date = date(2024, 1, 15)
        schedule.assign_employee_to_shift(emp, shift, work_date)
        assert schedule.is_employee_working(emp, work_date) is True
        assert schedule.is_employee_working(emp, date(2024, 1, 16)) is False
