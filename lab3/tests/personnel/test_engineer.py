"""
Тесты для класса Engineer
"""
import pytest
from factory.personnel.engineer import Engineer
from factory.production.machine import Machine


class TestEngineer:
    """Тесты для класса Engineer"""

    def test_engineer_creation(self):
        """Тест создания инженера"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        assert eng.name == "Alex Tech"
        assert eng.employee_id == "ENG-001"
        assert eng.salary == 70000
        assert eng.specialization == "Mechanical"
        assert eng.position == "Engineer"

    def test_assign_machine(self):
        """Тест назначения станка"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        machine = Machine("MACH-001", "Lathe", "CNC")
        eng.assign_machine(machine)
        assert machine in eng.machines

    def test_create_maintenance_request(self):
        """Тест создания заявки на обслуживание"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        machine = Machine("MACH-001", "Lathe", "CNC")
        # Updated signature: create_maintenance_request(machine, priority, description)
        result = eng.create_maintenance_request(machine, "high", "Oil change")
        assert result['priority'] == "high"
        assert result['description'] == "Oil change"
        assert result in eng.maintenance_requests

    def test_perform_maintenance(self):
        """Тест выполнения обслуживания"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        machine = Machine("MACH-001", "Lathe", "CNC")
        result = eng.perform_maintenance(machine)
        assert result['engineer'] == "Alex Tech"
        # Status is now 'completed' or 'requires_followup' depending on success
        assert result['status'] in ['completed', 'requires_followup']

    def test_add_technical_documentation(self):
        """Тест добавления технической документации"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        machine = Machine("MACH-001", "Lathe", "CNC")
        # Updated signature: add_technical_documentation(doc_name, machine, content)
        result = eng.add_technical_documentation("Maintenance Manual", machine, "Content here")
        assert result['name'] == "Maintenance Manual"
        assert result in eng.technical_docs

    def test_diagnose_problem(self):
        """Тест диагностики проблемы"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        machine = Machine("MACH-001", "Lathe", "CNC")
        result = eng.diagnose_problem(machine, "Strange noise")
        assert result['symptoms'] == "Strange noise"
        # diagnosis is now one of several possible values or 'requires_inspection'
        assert 'diagnosis' in result

    def test_get_assigned_machines_count(self):
        """Тест получения количества назначенных станков"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        assert eng.get_assigned_machines_count() == 0
        eng.assign_machine(Machine("M1", "M1", "T1"))
        eng.assign_machine(Machine("M2", "M2", "T2"))
        assert eng.get_assigned_machines_count() == 2

    def test_repr(self):
        """Тест строкового представления"""
        eng = Engineer("Alex Tech", "ENG-001", 70000, "Mechanical")
        assert "Alex Tech" in repr(eng)
        assert "Mechanical" in repr(eng)
