"""Тесты для класса Shift"""
import pytest
from factory.personnel.shift import Shift
from factory.personnel.worker import Worker
from factory.production.production_line import ProductionLine
from datetime import time


class TestShift:
    def test_creation(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        assert shift.name == "Morning"
        assert shift.is_active is False  # Changed: starts inactive

    def test_add_worker(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        worker = Worker("John", "W001", 40000)
        shift.add_worker(worker)
        assert worker in shift.workers
        assert worker.shift == shift

    def test_remove_worker(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        worker = Worker("John", "W001", 40000)
        shift.add_worker(worker)
        shift.remove_worker(worker)
        assert worker not in shift.workers

    def test_add_production_line(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        line = ProductionLine("L001", "Line 1")
        shift.add_production_line(line)
        assert line in shift.production_lines

    def test_get_worker_count(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        shift.add_worker(Worker("J1", "W1", 40000))
        shift.add_worker(Worker("J2", "W2", 40000))
        assert shift.get_worker_count() == 2

    def test_get_duration_hours(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        assert shift.get_duration_hours() == 8.0

    def test_start_shift(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        # Need to add at least one worker before starting
        worker = Worker("John", "W001", 40000)
        shift.add_worker(worker)
        result = shift.start_shift()
        assert result['shift'] == "Morning"
        assert shift.is_active is True

    def test_end_shift(self):
        shift = Shift("SH-001", "Morning", time(8, 0), time(16, 0))
        # Need to start shift before ending it
        worker = Worker("John", "W001", 40000)
        shift.add_worker(worker)
        shift.start_shift()
        result = shift.end_shift()
        assert shift.is_active is False
