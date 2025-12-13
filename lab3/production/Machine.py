"""
Станок/оборудование - производственное оборудование
"""
from datetime import datetime, timedelta
from typing import List, Dict
import random


class Machine:
    """Станок/оборудование"""

    def __init__(self, machine_id: str, name: str, machine_type: str):
        self.machine_id = machine_id
        self.name = name
        self.machine_type = machine_type
        self.production_line = None
        self.engineer = None
        self.maintenance_schedule = None
        self.operations = []
        self.maintenance_history = []
        self.breakdown_history = []
        self.is_operational = True
        self.last_maintenance = datetime.now()
        self.total_operations = 0
        self.total_runtime_hours = 0.0
        self.total_downtime_hours = 0.0
        self.wear_level = 0.0  # 0-100%
        self.efficiency_rating = 100.0  # 100% = новый станок
        self.purchase_date = datetime.now()
        self.warranty_expires = datetime.now() + timedelta(days=365)

    def assign_to_production_line(self, production_line):
        """
        Назначить на производственную линию

        Регистрирует станок на линии производства
        """
        if self.production_line is not None:
            print(f"Warning: Machine {self.name} is being transferred from line {self.production_line.name}")

        self.production_line = production_line

        print(f"Machine '{self.name}' assigned to production line '{production_line.name}'")

        return production_line

    def assign_engineer(self, engineer):
        """
        Назначить инженера с проверкой специализации

        Валидирует совместимость инженера с типом станка
        """
        if hasattr(engineer, 'specialization'):
            if engineer.specialization != "Universal" and engineer.specialization != self.machine_type:
                print(f"Warning: Engineer {engineer.name} ({engineer.specialization}) assigned to {self.machine_type} machine")

        self.engineer = engineer
        engineer.assign_machine(self)

        print(f"Engineer '{engineer.name}' assigned to machine '{self.name}'")

        return engineer

    def set_maintenance_schedule(self, schedule):
        """
        Установить график обслуживания

        Планирует регулярное техническое обслуживание
        """
        self.maintenance_schedule = schedule

        print(f"Maintenance schedule set for machine '{self.name}'")

        return schedule

    def add_operation(self, operation, duration_hours: float = 1.0):
        """
        Добавить операцию с отслеживанием износа

        Регистрирует работу станка и увеличивает износ
        """
        if not self.is_operational:
            raise RuntimeError(f"Cannot perform operation on non-operational machine {self.name}")

        operation_record = {
            'operation_id': f"OP-{self.total_operations + 1:06d}",
            'operation': operation,
            'timestamp': datetime.now(),
            'duration_hours': duration_hours,
            'wear_increase': round(duration_hours * 0.1, 2)  # 0.1% износа за час
        }

        self.operations.append(operation_record)
        self.total_operations += 1
        self.total_runtime_hours += duration_hours

        # Увеличение износа
        self.wear_level = min(100, self.wear_level + operation_record['wear_increase'])

        # Снижение эффективности при износе
        self.efficiency_rating = max(50, 100 - (self.wear_level * 0.5))

        # Симуляция поломки при критическом износе
        if self.wear_level > 80:
            breakdown_probability = (self.wear_level - 80) * 0.05  # До 100% при износе 100%
            if random.random() < breakdown_probability:
                self.breakdown("Critical wear level reached")

        print(f"Operation '{operation}' completed on {self.name}")
        print(f"Runtime: {duration_hours}h | Wear: {self.wear_level:.1f}% | Efficiency: {self.efficiency_rating:.1f}%")

        return operation_record

    def perform_maintenance(self, maintenance_type: str = "routine"):
        """
        Провести обслуживание с восстановлением характеристик

        Снижает износ и восстанавливает эффективность
        """
        if maintenance_type not in ["routine", "preventive", "overhaul"]:
            raise ValueError("Maintenance type must be 'routine', 'preventive', or 'overhaul'")

        # Эффект обслуживания
        wear_reduction = {
            "routine": 10,
            "preventive": 25,
            "overhaul": 60
        }

        maintenance_hours = {
            "routine": 2,
            "preventive": 4,
            "overhaul": 12
        }

        # Снижение износа
        old_wear = self.wear_level
        self.wear_level = max(0, self.wear_level - wear_reduction[maintenance_type])

        # Восстановление эффективности
        self.efficiency_rating = max(50, 100 - (self.wear_level * 0.5))

        # Восстановление работоспособности
        was_broken = not self.is_operational
        self.is_operational = True

        self.last_maintenance = datetime.now()

        maintenance_record = {
            'maintenance_id': f"MNT-{len(self.maintenance_history) + 1:05d}",
            'machine': self.name,
            'type': maintenance_type,
            'performed_at': datetime.now(),
            'duration_hours': maintenance_hours[maintenance_type],
            'wear_before': round(old_wear, 2),
            'wear_after': round(self.wear_level, 2),
            'repaired_breakdown': was_broken
        }

        self.maintenance_history.append(maintenance_record)

        if was_broken:
            print(f"Machine '{self.name}' repaired and restored to operation")
        else:
            print(f"{maintenance_type.title()} maintenance completed on '{self.name}'")

        print(f"Wear reduced: {old_wear:.1f}% -> {self.wear_level:.1f}% | Efficiency: {self.efficiency_rating:.1f}%")

        return maintenance_record

    def breakdown(self, reason: str = "Unknown failure"):
        """
        Поломка станка с регистрацией причины

        Останавливает работу и создает запись для анализа
        """
        if not self.is_operational:
            print(f"Warning: Machine {self.name} is already broken")
            return False

        self.is_operational = False

        breakdown_record = {
            'breakdown_id': f"BRK-{len(self.breakdown_history) + 1:05d}",
            'machine': self.name,
            'reason': reason,
            'broken_at': datetime.now(),
            'wear_level': round(self.wear_level, 2),
            'total_operations': self.total_operations,
            'days_since_maintenance': (datetime.now() - self.last_maintenance).days
        }

        self.breakdown_history.append(breakdown_record)

        print(f"MACHINE BREAKDOWN: {self.name}")
        print(f"Reason: {reason}")
        print(f"Wear level: {self.wear_level:.1f}%")

        # Уведомление инженера
        if self.engineer:
            print(f"Engineer {self.engineer.name} notified")

        return breakdown_record

    def repair(self, repair_duration_hours: float = 4.0):
        """
        Починить станок после поломки

        Восстанавливает работоспособность и записывает время простоя
        """
        if self.is_operational:
            print(f"Warning: Machine {self.name} is already operational")
            return False

        # Проверка последней поломки
        if self.breakdown_history:
            last_breakdown = self.breakdown_history[-1]
            downtime = (datetime.now() - last_breakdown['broken_at']).total_seconds() / 3600
            self.total_downtime_hours += downtime
        else:
            downtime = 0

        self.is_operational = True

        repair_record = {
            'machine': self.name,
            'repaired_at': datetime.now(),
            'repair_duration_hours': repair_duration_hours,
            'total_downtime_hours': round(downtime, 2)
        }

        print(f"Machine '{self.name}' repaired successfully")
        print(f"Downtime: {downtime:.2f}h | Repair time: {repair_duration_hours:.2f}h")

        return repair_record

    def get_uptime_percentage(self):
        """
        Рассчитать процент работоспособности

        Учитывает время работы и простоя
        """
        if not self.is_operational:
            return 0.0

        total_time = self.total_runtime_hours + self.total_downtime_hours

        if total_time == 0:
            return 100.0

        uptime = (self.total_runtime_hours / total_time) * 100

        return round(uptime, 2)

    def needs_maintenance(self) -> bool:
        """
        Проверить необходимость обслуживания

        Учитывает время, износ и количество операций
        """
        days_since_maintenance = (datetime.now() - self.last_maintenance).days

        # Критерии для обслуживания
        time_exceeded = days_since_maintenance > 30
        wear_high = self.wear_level > 60
        operations_high = self.total_operations > 1000

        needs_service = time_exceeded or wear_high or operations_high

        if needs_service:
            reasons = []
            if time_exceeded:
                reasons.append(f"{days_since_maintenance} days since last maintenance")
            if wear_high:
                reasons.append(f"wear level {self.wear_level:.1f}%")
            if operations_high:
                reasons.append(f"{self.total_operations} operations performed")

            print(f"Machine '{self.name}' requires maintenance:")
            for reason in reasons:
                print(f"  - {reason}")

        return needs_service

    def get_remaining_warranty_days(self) -> int:
        """Получить оставшиеся дни гарантии"""
        if datetime.now() > self.warranty_expires:
            return 0

        remaining = (self.warranty_expires - datetime.now()).days
        return max(0, remaining)

    def is_under_warranty(self) -> bool:
        """Проверить действие гарантии"""
        return datetime.now() < self.warranty_expires

    def get_machine_statistics(self) -> Dict:
        """
        Получить полную статистику станка

        Возвращает детальную информацию о работе
        """
        age_days = (datetime.now() - self.purchase_date).days

        stats = {
            'machine_id': self.machine_id,
            'machine_name': self.name,
            'machine_type': self.machine_type,
            'is_operational': self.is_operational,
            'age_days': age_days,
            'wear_level': round(self.wear_level, 2),
            'efficiency_rating': round(self.efficiency_rating, 2),
            'total_operations': self.total_operations,
            'total_runtime_hours': round(self.total_runtime_hours, 2),
            'total_downtime_hours': round(self.total_downtime_hours, 2),
            'uptime_percentage': self.get_uptime_percentage(),
            'days_since_maintenance': (datetime.now() - self.last_maintenance).days,
            'needs_maintenance': self.needs_maintenance(),
            'total_breakdowns': len(self.breakdown_history),
            'total_maintenances': len(self.maintenance_history),
            'under_warranty': self.is_under_warranty(),
            'warranty_days_remaining': self.get_remaining_warranty_days(),
            'assigned_engineer': self.engineer.name if self.engineer else None,
            'production_line': self.production_line.name if self.production_line else None
        }

        return stats

    def reset_after_overhaul(self):
        """
        Сброс статистики после капитального ремонта

        Обновляет счетчики как для нового оборудования
        """
        self.wear_level = 0.0
        self.efficiency_rating = 100.0
        self.total_operations = 0
        self.total_runtime_hours = 0.0
        self.total_downtime_hours = 0.0
        self.is_operational = True
        self.last_maintenance = datetime.now()

        print(f"Machine '{self.name}' overhauled - statistics reset")
        print("Machine restored to like-new condition")

    def __repr__(self):
        return f"Machine(name='{self.name}', type='{self.machine_type}', operational={self.is_operational}, wear={self.wear_level:.1f}%)"
