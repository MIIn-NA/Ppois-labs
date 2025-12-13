"""Тесты для ProductionLine"""
import pytest
from factory.production.production_line import ProductionLine
from factory.management.factory import Factory
from factory.production.machine import Machine
from factory.personnel.worker import Worker
from factory.products.product import Product


class TestProductionLine:
    def test_creation(self):
        line = ProductionLine("L001", "Assembly Line")
        assert line.line_id == "L001"
        assert line.name == "Assembly Line"
        assert line.is_operational is False  # Changed: starts non-operational

    def test_assign_to_factory(self):
        line = ProductionLine("L001", "Assembly")
        factory = Factory("Factory", "Moscow")
        line.assign_to_factory(factory)
        assert line.factory == factory
        assert line in factory.production_lines

    def test_add_machine(self):
        line = ProductionLine("L001", "Assembly")
        machine = Machine("M001", "Lathe", "CNC")
        line.add_machine(machine)
        assert machine in line.machines
        assert machine.production_line == line

    def test_add_worker(self):
        line = ProductionLine("L001", "Assembly")
        worker = Worker("John", "W001", 40000)
        line.add_worker(worker)
        assert worker in line.workers
        assert worker.production_line == line

    def test_start_stop_production(self):
        line = ProductionLine("L001", "Assembly")
        # Need to add minimum resources before starting
        for i in range(2):  # min_machines_required = 2
            machine = Machine(f"M{i}", f"Machine{i}", "Type")
            line.add_machine(machine)
        for i in range(3):  # min_workers_required = 3
            worker = Worker(f"Worker{i}", f"W{i}", 40000)
            line.add_worker(worker)

        result = line.start_production()
        assert line.is_operational is True
        line.stop_production()
        assert line.is_operational is False

    def test_increase_production_volume(self):
        line = ProductionLine("L001", "Assembly")
        line.increase_production_volume(100)
        assert line.production_volume == 100

    def test_get_efficiency(self):
        line = ProductionLine("L001", "Assembly")
        m1 = Machine("M1", "M1", "T1")
        m2 = Machine("M2", "M2", "T2")
        m1.is_operational = True
        m2.is_operational = False
        line.add_machine(m1)
        line.add_machine(m2)
        # New efficiency calculation: (machine_eff * 0.6) + (worker_eff * 0.4)
        # Machine efficiency: 50% (1 of 2 operational)
        # Worker efficiency: 0% (no workers, min required is 3)
        # Result: 50 * 0.6 + 0 * 0.4 = 30.0
        assert line.get_efficiency() == 30.0
