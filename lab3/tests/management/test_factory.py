"""
Тесты для класса Factory
"""
import pytest
from factory.management.factory import Factory
from factory.management.department import Department
from factory.production.production_line import ProductionLine
from factory.warehouse.warehouse import Warehouse
from factory.quality.quality_control import QualityControl
from factory.finance.finance_department import FinanceDepartment


class TestFactory:
    """Тесты для класса Factory"""

    def test_factory_creation(self):
        """Тест создания фабрики"""
        factory = Factory("Test Factory", "Moscow, Russia")
        assert factory.name == "Test Factory"
        assert factory.address == "Moscow, Russia"
        assert factory.is_operational is True
        assert len(factory.production_lines) == 0
        assert factory.total_employees == 0
        assert factory.monthly_revenue == 0.0
        assert factory.monthly_expenses == 0.0

    def test_add_production_line_success(self, capsys):
        """Тест успешного добавления производственной линии"""
        factory = Factory("Test Factory", "Moscow")
        line = ProductionLine("LINE-001", "Assembly Line")
        result = factory.add_production_line(line)

        assert len(factory.production_lines) == 1
        assert line in factory.production_lines
        assert line.factory == factory
        assert result == line

        # Проверка логирования
        captured = capsys.readouterr()
        assert "Added production line" in captured.out

    def test_add_production_line_duplicate_id(self):
        """Тест добавления линии с дублирующимся ID"""
        factory = Factory("Test Factory", "Moscow")
        line1 = ProductionLine("LINE-001", "Line 1")
        line2 = ProductionLine("LINE-001", "Line 2")

        factory.add_production_line(line1)

        with pytest.raises(ValueError, match="already exists"):
            factory.add_production_line(line2)

    def test_add_production_line_to_shutdown_factory(self):
        """Тест добавления линии к остановленной фабрике"""
        factory = Factory("Test Factory", "Moscow")
        factory.is_operational = False
        line = ProductionLine("LINE-001", "Assembly")

        with pytest.raises(RuntimeError, match="non-operational factory"):
            factory.add_production_line(line)

    def test_add_warehouse_success(self, capsys):
        """Тест успешного добавления склада"""
        factory = Factory("Test Factory", "Moscow")
        warehouse = Warehouse("WH-001", "Main Warehouse", 1000.0)
        result = factory.add_warehouse(warehouse)

        assert len(factory.warehouses) == 1
        assert warehouse in factory.warehouses
        assert warehouse.factory == factory
        assert result == warehouse

        captured = capsys.readouterr()
        assert "Added warehouse" in captured.out

    def test_add_warehouse_invalid_capacity(self):
        """Тест добавления склада с некорректной емкостью"""
        factory = Factory("Test Factory", "Moscow")
        warehouse = Warehouse("WH-001", "Bad Warehouse", -100.0)

        with pytest.raises(ValueError, match="capacity must be positive"):
            factory.add_warehouse(warehouse)

    def test_add_warehouse_duplicate_id(self):
        """Тест добавления склада с дублирующимся ID"""
        factory = Factory("Test Factory", "Moscow")
        wh1 = Warehouse("WH-001", "Warehouse 1", 1000.0)
        wh2 = Warehouse("WH-001", "Warehouse 2", 2000.0)

        factory.add_warehouse(wh1)

        with pytest.raises(ValueError, match="already exists"):
            factory.add_warehouse(wh2)

    def test_add_department_success(self, capsys):
        """Тест успешного добавления отдела"""
        factory = Factory("Test Factory", "Moscow")
        dept = Department("HR", "DEPT-001")

        # Добавим сотрудников в отдел
        from factory.personnel.employee import Employee
        emp1 = Employee("John", "E1", 50000)
        emp2 = Employee("Jane", "E2", 60000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)

        result = factory.add_department(dept)

        assert len(factory.departments) == 1
        assert dept in factory.departments
        assert factory.total_employees == 2
        assert result == dept

        captured = capsys.readouterr()
        assert "Added department" in captured.out
        assert "2 employees" in captured.out

    def test_add_department_duplicate_id(self):
        """Тест добавления отдела с дублирующимся ID"""
        factory = Factory("Test Factory", "Moscow")
        dept1 = Department("HR", "DEPT-001")
        dept2 = Department("IT", "DEPT-001")

        factory.add_department(dept1)

        with pytest.raises(ValueError, match="already exists"):
            factory.add_department(dept2)

    def test_set_finance_department(self, capsys):
        """Тест установки финансового отдела"""
        factory = Factory("Test Factory", "Moscow")
        finance_dept = FinanceDepartment("FIN-001", "Finance")

        result = factory.set_finance_department(finance_dept)

        assert factory.finance_department == finance_dept
        assert finance_dept.factory == factory
        assert result == finance_dept

    def test_set_quality_control(self, capsys):
        """Тест установки контроля качества"""
        factory = Factory("Test Factory", "Moscow")
        qc = QualityControl("QC-001", "Quality Control")

        result = factory.set_quality_control(qc)

        assert factory.quality_control == qc
        assert qc.factory == factory
        assert result == qc

    def test_get_total_production(self):
        """Тест получения общего объема производства"""
        factory = Factory("Test Factory", "Moscow")
        line1 = ProductionLine("LINE-001", "Line 1")
        line1.production_volume = 100
        line2 = ProductionLine("LINE-002", "Line 2")
        line2.production_volume = 150

        factory.production_lines.append(line1)
        factory.production_lines.append(line2)

        assert factory.get_total_production() == 250

    def test_get_total_production_empty(self):
        """Тест получения производства при отсутствии линий"""
        factory = Factory("Test Factory", "Moscow")
        assert factory.get_total_production() == 0

    def test_calculate_efficiency(self):
        """Тест расчета эффективности фабрики"""
        factory = Factory("Test Factory", "Moscow")

        # Добавляем линию
        line = ProductionLine("LINE-001", "Line 1")
        from factory.production.machine import Machine
        m1 = Machine("M1", "Machine 1", "Type1")
        m1.is_operational = True
        m2 = Machine("M2", "Machine 2", "Type2")
        m2.is_operational = True
        line.machines = [m1, m2]
        factory.production_lines.append(line)

        # Добавляем склад
        warehouse = Warehouse("WH-001", "Warehouse", 1000.0)
        warehouse.current_utilization = 600.0
        factory.warehouses.append(warehouse)

        # Добавляем контроль качества
        qc = QualityControl("QC-001", "QC")
        qc.total_inspections = 100
        qc.total_passed = 95
        factory.quality_control = qc

        efficiency = factory.calculate_efficiency()

        assert isinstance(efficiency, float)
        assert 0 <= efficiency <= 100

    def test_calculate_efficiency_no_lines(self):
        """Тест расчета эффективности без линий"""
        factory = Factory("Test Factory", "Moscow")
        assert factory.calculate_efficiency() == 0.0

    def test_get_status_report(self):
        """Тест получения отчета о состоянии"""
        factory = Factory("Test Factory", "Moscow")
        factory.monthly_revenue = 100000.0
        factory.monthly_expenses = 60000.0

        line = ProductionLine("LINE-001", "Line 1")
        factory.production_lines.append(line)

        dept = Department("HR", "DEPT-001")
        factory.departments.append(dept)

        report = factory.get_status_report()

        assert report['factory_name'] == "Test Factory"
        assert report['is_operational'] is True
        assert report['production_lines'] == 1
        assert report['departments'] == 1
        assert report['monthly_revenue'] == 100000.0
        assert report['monthly_expenses'] == 60000.0
        assert report['net_profit'] == 40000.0
        assert 'uptime_days' in report

    def test_shutdown(self, capsys):
        """Тест остановки фабрики"""
        factory = Factory("Test Factory", "Moscow")
        line = ProductionLine("LINE-001", "Line 1")
        factory.production_lines.append(line)

        result = factory.shutdown()

        assert result is True
        assert factory.is_operational is False

        captured = capsys.readouterr()
        assert "shutdown" in captured.out.lower()

    def test_shutdown_already_stopped(self, capsys):
        """Тест остановки уже остановленной фабрики"""
        factory = Factory("Test Factory", "Moscow")
        factory.is_operational = False

        result = factory.shutdown()

        assert result is False
        captured = capsys.readouterr()
        assert "already shut down" in captured.out

    def test_start_success(self, capsys):
        """Тест успешного запуска фабрики"""
        factory = Factory("Test Factory", "Moscow")
        factory.is_operational = False

        line = ProductionLine("LINE-001", "Line 1")
        # Production lines now require minimum resources before starting
        from factory.production.machine import Machine
        from factory.personnel.worker import Worker
        # Add minimum required machines (min_machines_required = 2)
        for i in range(2):
            machine = Machine(f"M{i}", f"Machine{i}", "Type")
            line.add_machine(machine)
        # Add minimum required workers (min_workers_required = 3)
        for i in range(3):
            worker = Worker(f"Worker{i}", f"W{i}", 40000)
            line.add_worker(worker)

        factory.production_lines.append(line)

        warehouse = Warehouse("WH-001", "Warehouse", 1000.0)
        factory.warehouses.append(warehouse)

        result = factory.start()

        assert result is True
        assert factory.is_operational is True

        captured = capsys.readouterr()
        assert "started successfully" in captured.out.lower()

    def test_start_already_running(self, capsys):
        """Тест запуска уже работающей фабрики"""
        factory = Factory("Test Factory", "Moscow")

        result = factory.start()

        assert result is False
        captured = capsys.readouterr()
        assert "already operational" in captured.out

    def test_start_no_production_lines(self):
        """Тест запуска без производственных линий"""
        factory = Factory("Test Factory", "Moscow")
        factory.is_operational = False

        with pytest.raises(RuntimeError, match="no production lines"):
            factory.start()

    def test_start_no_warehouses(self):
        """Тест запуска без складов"""
        factory = Factory("Test Factory", "Moscow")
        factory.is_operational = False

        line = ProductionLine("LINE-001", "Line 1")
        factory.production_lines.append(line)

        with pytest.raises(RuntimeError, match="no warehouses"):
            factory.start()

    def test_record_quality_incident(self):
        """Тест записи инцидента качества"""
        factory = Factory("Test Factory", "Moscow")
        incident = {
            'type': 'defect',
            'severity': 'high',
            'description': 'Surface defect found'
        }

        factory.record_quality_incident(incident)

        assert len(factory.quality_incidents) == 1
        assert 'recorded_at' in factory.quality_incidents[0]

    def test_update_financials(self):
        """Тест обновления финансовых показателей"""
        factory = Factory("Test Factory", "Moscow")

        factory.update_financials(150000.0, 90000.0)

        assert factory.monthly_revenue == 150000.0
        assert factory.monthly_expenses == 90000.0

    def test_repr(self):
        """Тест строкового представления"""
        factory = Factory("Test Factory", "Moscow")
        line = ProductionLine("LINE-001", "Line 1")
        factory.production_lines.append(line)

        repr_str = repr(factory)

        assert "Test Factory" in repr_str
        assert "lines=1" in repr_str
        assert "operational=True" in repr_str
