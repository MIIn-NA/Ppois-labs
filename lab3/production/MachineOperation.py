"""
Операция на станке - конкретная производственная операция
"""
from datetime import datetime


class MachineOperation:
    """Операция на станке"""

    def __init__(self, operation_id: str, operation_type: str):
        self.operation_id = operation_id
        self.operation_type = operation_type
        self.machine = None
        self.worker = None
        self.product = None
        self.operation_time = 0  # в минутах
        self.start_time = None
        self.end_time = None
        self.status = "pending"  # pending, in_progress, completed, failed

    def assign_machine(self, machine):
        """Назначить станок"""
        self.machine = machine
        machine.add_operation(self)

    def assign_worker(self, worker):
        """Назначить рабочего"""
        self.worker = worker

    def assign_product(self, product):
        """Назначить продукт"""
        self.product = product

    def set_operation_time(self, minutes: int):
        """Установить время операции"""
        self.operation_time = minutes

    def start(self):
        """Начать операцию"""
        self.status = "in_progress"
        self.start_time = datetime.now()
        return {'operation': self.operation_type, 'started_at': self.start_time}

    def complete(self):
        """Завершить операцию"""
        self.status = "completed"
        self.end_time = datetime.now()
        return {'operation': self.operation_type, 'completed_at': self.end_time}

    def fail(self, reason: str):
        """Провалить операцию"""
        self.status = "failed"
        return {'operation': self.operation_type, 'failed_at': datetime.now(), 'reason': reason}

    def get_actual_duration(self):
        """Получить фактическую продолжительность"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 60  # в минутах
        return 0

    def __repr__(self):
        return f"MachineOperation(type='{self.operation_type}', status='{self.status}')"
