"""Тесты для MachineOperation"""
import pytest
from factory.production.machine_operation import MachineOperation
from factory.production.machine import Machine


class TestMachineOperation:
    def test_creation(self):
        op = MachineOperation("OP001", "drilling")
        assert op.operation_id == "OP001"
        assert op.status == "pending"

    def test_start_complete(self):
        op = MachineOperation("OP001", "drilling")
        op.start()
        assert op.status == "in_progress"
        op.complete()
        assert op.status == "completed"

    def test_fail(self):
        op = MachineOperation("OP001", "drilling")
        op.fail("Machine error")
        assert op.status == "failed"

    def test_get_actual_duration(self):
        op = MachineOperation("OP001", "drilling")
        op.start()
        op.complete()
        duration = op.get_actual_duration()
        assert duration >= 0
