"""
Тесты для класса Worker
"""
import pytest
from factory.personnel.worker import Worker
from factory.production.production_line import ProductionLine
from factory.production.machine import Machine
from factory.personnel.shift import Shift
from datetime import time


class TestWorker:
    """Тесты для класса Worker"""

    def test_worker_creation(self):
        """Тест создания рабочего"""
        worker = Worker("Ivan Petrov", "WRK-001", 45000)
        assert worker.name == "Ivan Petrov"
        assert worker.employee_id == "WRK-001"
        assert worker.salary == 45000
        assert worker.base_salary == 45000
        assert worker.skill_level == 1
        assert worker.position == "Worker"
        assert worker.experience_days == 0
        assert worker.total_operations_count == 0

    def test_assign_to_production_line_success(self, capsys):
        """Тест успешного назначения на линию"""
        worker = Worker("Ivan", "WRK-001", 45000)
        line = ProductionLine("LINE-001", "Assembly")
        
        result = worker.assign_to_production_line(line)
        
        assert worker.production_line == line
        assert result == line
        captured = capsys.readouterr()
        assert "assigned to line" in captured.out

    def test_assign_inactive_worker_to_line(self):
        """Тест назначения неактивного рабочего"""
        worker = Worker("Ivan", "WRK-001", 45000)
        worker.is_active = False
        line = ProductionLine("LINE-001", "Assembly")
        
        with pytest.raises(RuntimeError, match="inactive worker"):
            worker.assign_to_production_line(line)

    def test_assign_machine_success(self, capsys):
        """Тест успешного назначения станка"""
        worker = Worker("Ivan", "WRK-001", 45000)
        line = ProductionLine("LINE-001", "Assembly")
        machine = Machine("MACH-001", "Lathe", "CNC")
        
        worker.assign_to_production_line(line)
        result = worker.assign_machine(machine)
        
        assert worker.machine == machine
        assert result == machine
        captured = capsys.readouterr()
        assert "assigned to machine" in captured.out

    def test_assign_machine_without_line(self):
        """Тест назначения станка без линии"""
        worker = Worker("Ivan", "WRK-001", 45000)
        machine = Machine("MACH-001", "Lathe", "CNC")
        
        with pytest.raises(RuntimeError, match="production line first"):
            worker.assign_machine(machine)

    def test_assign_non_operational_machine(self):
        """Тест назначения неработающего станка"""
        worker = Worker("Ivan", "WRK-001", 45000)
        line = ProductionLine("LINE-001", "Assembly")
        machine = Machine("MACH-001", "Lathe", "CNC")
        machine.is_operational = False
        
        worker.assign_to_production_line(line)
        
        with pytest.raises(ValueError, match="non-operational machine"):
            worker.assign_machine(machine)

    def test_perform_operation_success(self, capsys):
        """Тест выполнения операции"""
        worker = Worker("Ivan", "WRK-001", 45000)
        line = ProductionLine("LINE-001", "Assembly")
        machine = Machine("MACH-001", "Lathe", "CNC")
        
        worker.assign_to_production_line(line)
        worker.assign_machine(machine)
        
        result = worker.perform_operation("drilling")
        
        assert result['worker'] == "Ivan"
        assert result['operation'] == "drilling"
        assert 'duration_minutes' in result
        assert 'quality_score' in result
        assert worker.total_operations_count == 1
        assert worker.experience_days > 0
        
        captured = capsys.readouterr()
        assert "Completed" in captured.out

    def test_perform_operation_without_setup(self):
        """Тест выполнения операции без подготовки"""
        worker = Worker("Ivan", "WRK-001", 45000)
        
        with pytest.raises(RuntimeError, match="must have assigned"):
            worker.perform_operation("drilling")

    def test_increase_skill_level_success(self, capsys):
        """Тест повышения квалификации"""
        worker = Worker("Ivan", "WRK-001", 45000)
        worker.experience_days = 150  # Достаточно опыта
        
        result = worker.increase_skill_level()
        
        assert result is True
        assert worker.skill_level == 2
        assert worker.salary > 45000  # Зарплата увеличилась
        
        captured = capsys.readouterr()
        assert "promoted" in captured.out

    def test_increase_skill_level_insufficient_exp(self):
        """Тест повышения без достаточного опыта"""
        worker = Worker("Ivan", "WRK-001", 45000)
        worker.experience_days = 50  # Недостаточно
        
        with pytest.raises(ValueError, match="Insufficient experience"):
            worker.increase_skill_level()

    def test_increase_skill_level_max_level(self, capsys):
        """Тест повышения при максимальном уровне"""
        worker = Worker("Ivan", "WRK-001", 45000)
        worker.skill_level = 5
        
        result = worker.increase_skill_level()
        
        assert result is False
        captured = capsys.readouterr()
        assert "maximum" in captured.out

    def test_add_training_course(self, capsys):
        """Тест прохождения обучения"""
        worker = Worker("Ivan", "WRK-001", 45000)
        
        course = worker.add_training_course("Advanced CNC Operations")
        
        assert len(worker.training_courses) == 1
        assert course['name'] == "Advanced CNC Operations"
        assert worker.experience_days == 30
        
        captured = capsys.readouterr()
        assert "completed training" in captured.out

    def test_record_overtime(self, capsys):
        """Тест записи переработки"""
        worker = Worker("Ivan", "WRK-001", 48000)
        
        pay = worker.record_overtime(3.0)
        
        assert worker.overtime_hours == 3.0
        assert pay > 0
        assert worker.bonus_amount == pay
        
        captured = capsys.readouterr()
        assert "overtime" in captured.out

    def test_record_invalid_overtime(self):
        """Тест записи некорректной переработки"""
        worker = Worker("Ivan", "WRK-001", 45000)
        
        with pytest.raises(ValueError, match="must be positive"):
            worker.record_overtime(-2.0)

    def test_record_excessive_overtime(self, capsys):
        """Тест записи чрезмерной переработки"""
        worker = Worker("Ivan", "WRK-001", 45000)
        
        worker.record_overtime(5.0)
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Excessive" in captured.out

    def test_calculate_total_salary(self):
        """Тест расчета общей зарплаты"""
        worker = Worker("Ivan", "WRK-001", 50000)
        worker.performance_rating = 0.9
        worker.record_overtime(2.0)
        
        salary = worker.calculate_total_salary()
        
        assert salary['base_salary'] == 50000
        assert salary['performance_bonus'] > 0
        assert salary['overtime_bonus'] > 0
        assert salary['total'] > 50000

    def test_get_productivity(self):
        """Тест расчета производительности"""
        worker = Worker("Ivan", "WRK-001", 45000)
        worker.experience_days = 100
        worker.skill_level = 3
        
        productivity = worker.get_productivity()
        
        assert isinstance(productivity, float)
        assert productivity > 0

    def test_get_statistics(self):
        """Тест получения статистики"""
        worker = Worker("Ivan", "WRK-001", 45000)
        line = ProductionLine("LINE-001", "Assembly")
        worker.assign_to_production_line(line)
        
        stats = worker.get_statistics()
        
        assert stats['name'] == "Ivan"
        assert stats['skill_level'] == 1
        assert stats['production_line'] == "Assembly"
        assert 'productivity' in stats
        assert 'total_salary' in stats
        assert 'work_days' in stats

    def test_reset_monthly_stats(self, capsys):
        """Тест сброса месячной статистики"""
        worker = Worker("Ivan", "WRK-001", 45000)
        worker.overtime_hours = 10.0
        worker.bonus_amount = 5000.0
        
        worker.reset_monthly_stats()
        
        assert worker.overtime_hours == 0.0
        assert worker.bonus_amount == 0.0
        
        captured = capsys.readouterr()
        assert "reset" in captured.out

    def test_repr(self):
        """Тест строкового представления"""
        worker = Worker("Ivan Petrov", "WRK-001", 45000)
        
        repr_str = repr(worker)
        
        assert "Ivan Petrov" in repr_str
        assert "skill_level=1" in repr_str
        assert "productivity=" in repr_str
