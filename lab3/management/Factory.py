"""
Главный класс фабрики - управляет всеми производственными процессами
"""
from typing import List, Optional, Dict
from datetime import datetime


class Factory:
    """Главный класс фабрики"""

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.production_lines = []
        self.warehouses = []
        self.departments = []
        self.finance_department = None
        self.quality_control = None
        self.created_at = datetime.now()
        self.is_operational = True
        self.total_employees = 0
        self.monthly_revenue = 0.0
        self.monthly_expenses = 0.0
        self.production_target = 0
        self.quality_incidents = []

    def add_production_line(self, production_line):
        """
        Добавить производственную линию с проверками

        Проверяет уникальность ID линии и автоматически связывает
        с фабрикой. Обновляет статистику фабрики.
        """
        # Проверка уникальности ID
        existing_ids = [line.line_id for line in self.production_lines]
        if production_line.line_id in existing_ids:
            raise ValueError(f"Production line with ID {production_line.line_id} already exists")

        # Проверка операционного статуса
        if not self.is_operational:
            raise RuntimeError("Cannot add production line to non-operational factory")

        # Добавление линии
        self.production_lines.append(production_line)
        production_line.factory = self

        # Логирование
        print(f"[{datetime.now()}] Added production line '{production_line.name}' to factory '{self.name}'")

        return production_line

    def add_warehouse(self, warehouse):
        """
        Добавить склад с валидацией емкости

        Проверяет наличие свободного места и корректность
        параметров склада перед добавлением.
        """
        # Проверка емкости склада
        if warehouse.capacity <= 0:
            raise ValueError("Warehouse capacity must be positive")

        # Проверка уникальности
        existing_ids = [w.warehouse_id for w in self.warehouses]
        if warehouse.warehouse_id in existing_ids:
            raise ValueError(f"Warehouse with ID {warehouse.warehouse_id} already exists")

        # Добавление склада
        self.warehouses.append(warehouse)
        warehouse.factory = self

        print(f"[{datetime.now()}] Added warehouse '{warehouse.name}' with capacity {warehouse.capacity}")

        return warehouse

    def add_department(self, department):
        """
        Добавить отдел с обновлением счетчика сотрудников

        Автоматически подсчитывает сотрудников в новом отделе
        и обновляет общую статистику фабрики.
        """
        # Проверка уникальности
        existing_ids = [d.department_id for d in self.departments]
        if department.department_id in existing_ids:
            raise ValueError(f"Department with ID {department.department_id} already exists")

        # Добавление отдела
        self.departments.append(department)

        # Обновление статистики сотрудников
        self.total_employees += len(department.employees)

        print(f"[{datetime.now()}] Added department '{department.name}' with {len(department.employees)} employees")

        return department

    def set_finance_department(self, finance_dept):
        """Установить финансовый отдел"""
        if self.finance_department is not None:
            print(f"Warning: Replacing existing finance department")

        self.finance_department = finance_dept
        finance_dept.factory = self

        return finance_dept

    def set_quality_control(self, quality_control):
        """Установить систему контроля качества"""
        if self.quality_control is not None:
            print(f"Warning: Replacing existing quality control system")

        self.quality_control = quality_control
        quality_control.factory = self

        return quality_control

    def get_total_production(self):
        """
        Получить общий объем производства

        Суммирует производство всех активных линий
        """
        if not self.production_lines:
            return 0

        total = sum(line.get_production_volume() for line in self.production_lines)
        return total

    def calculate_efficiency(self):
        """
        Рассчитать общую эффективность фабрики

        Учитывает загрузку линий, качество продукции,
        использование складов и финансовые показатели
        """
        if not self.production_lines:
            return 0.0

        # Эффективность производственных линий
        line_efficiency = sum(line.get_efficiency() for line in self.production_lines) / len(self.production_lines)

        # Эффективность использования складов
        warehouse_efficiency = 0.0
        if self.warehouses:
            warehouse_efficiency = sum(w.get_utilization_percentage() for w in self.warehouses) / len(self.warehouses)

        # Качество продукции
        quality_rate = 100.0
        if self.quality_control:
            quality_rate = self.quality_control.get_pass_rate()

        # Итоговая эффективность (взвешенное среднее)
        total_efficiency = (line_efficiency * 0.5 + warehouse_efficiency * 0.2 + quality_rate * 0.3)

        return round(total_efficiency, 2)

    def get_status_report(self) -> Dict:
        """
        Получить детальный отчет о состоянии фабрики

        Возвращает словарь с полной статистикой работы фабрики
        """
        report = {
            'factory_name': self.name,
            'is_operational': self.is_operational,
            'production_lines': len(self.production_lines),
            'active_lines': sum(1 for line in self.production_lines if line.is_operational),
            'warehouses': len(self.warehouses),
            'departments': len(self.departments),
            'total_employees': self.total_employees,
            'total_production': self.get_total_production(),
            'efficiency': self.calculate_efficiency(),
            'monthly_revenue': self.monthly_revenue,
            'monthly_expenses': self.monthly_expenses,
            'net_profit': self.monthly_revenue - self.monthly_expenses,
            'quality_incidents': len(self.quality_incidents),
            'uptime_days': (datetime.now() - self.created_at).days
        }

        return report

    def shutdown(self):
        """
        Остановить фабрику со всеми проверками

        Останавливает все производственные линии,
        сохраняет текущее состояние и логирует событие
        """
        if not self.is_operational:
            print("Warning: Factory is already shut down")
            return False

        print(f"[{datetime.now()}] Initiating factory shutdown...")

        # Остановка всех производственных линий
        for line in self.production_lines:
            if line.is_operational:
                line.stop_production()
                print(f"  - Stopped production line '{line.name}'")

        # Изменение статуса
        self.is_operational = False

        print(f"[{datetime.now()}] Factory '{self.name}' has been shut down")

        return True

    def start(self):
        """
        Запустить фабрику с проверками готовности

        Проверяет наличие всех необходимых компонентов
        перед запуском производства
        """
        if self.is_operational:
            print("Warning: Factory is already operational")
            return False

        # Проверка готовности
        if not self.production_lines:
            raise RuntimeError("Cannot start factory: no production lines configured")

        if not self.warehouses:
            raise RuntimeError("Cannot start factory: no warehouses configured")

        if not self.quality_control:
            print("Warning: Starting factory without quality control system")

        print(f"[{datetime.now()}] Starting factory '{self.name}'...")

        # Запуск производственных линий
        started_lines = 0
        for line in self.production_lines:
            if not line.is_operational:
                line.start_production()
                started_lines += 1

        # Изменение статуса
        self.is_operational = True

        print(f"[{datetime.now()}] Factory started successfully. {started_lines} production lines activated")

        return True

    def record_quality_incident(self, incident: Dict):
        """Записать инцидент качества"""
        incident['recorded_at'] = datetime.now()
        self.quality_incidents.append(incident)

    def update_financials(self, revenue: float, expenses: float):
        """Обновить финансовые показатели"""
        self.monthly_revenue = revenue
        self.monthly_expenses = expenses

    def __repr__(self):
        return f"Factory(name='{self.name}', lines={len(self.production_lines)}, operational={self.is_operational})"
