"""
Заявка на ремонт - запрос на техническое обслуживание
"""
from datetime import datetime


class MaintenanceRequest:
    """Заявка на ремонт"""

    def __init__(self, request_id: str, description: str, priority: str = "medium"):
        self.request_id = request_id
        self.description = description
        self.priority = priority  # low, medium, high, urgent
        self.machine = None
        self.engineer = None
        self.maintenance_schedule = None
        self.created_at = datetime.now()
        self.completed_at = None
        self.status = "pending"  # pending, assigned, in_progress, completed, cancelled

    def assign_machine(self, machine):
        """Назначить станок"""
        self.machine = machine

    def assign_engineer(self, engineer):
        """Назначить инженера"""
        self.engineer = engineer
        engineer.create_maintenance_request(self)
        self.status = "assigned"

    def set_maintenance_schedule(self, schedule):
        """Установить график обслуживания"""
        self.maintenance_schedule = schedule
        schedule.add_maintenance_request(self)

    def start_work(self):
        """Начать работу"""
        self.status = "in_progress"
        return {'request': self.request_id, 'started_at': datetime.now()}

    def complete(self):
        """Завершить заявку"""
        self.status = "completed"
        self.completed_at = datetime.now()
        if self.machine:
            self.machine.perform_maintenance()
        return {'request': self.request_id, 'completed_at': self.completed_at}

    def cancel(self, reason: str):
        """Отменить заявку"""
        self.status = "cancelled"
        return {'request': self.request_id, 'cancelled_at': datetime.now(), 'reason': reason}

    def escalate_priority(self):
        """Повысить приоритет"""
        priority_levels = ['low', 'medium', 'high', 'urgent']
        current_index = priority_levels.index(self.priority)
        if current_index < len(priority_levels) - 1:
            self.priority = priority_levels[current_index + 1]

    def get_duration(self):
        """Получить длительность выполнения"""
        if self.completed_at:
            delta = self.completed_at - self.created_at
            return delta.total_seconds() / 3600  # в часах
        return 0

    def __repr__(self):
        return f"MaintenanceRequest(id='{self.request_id}', priority='{self.priority}', status='{self.status}')"
