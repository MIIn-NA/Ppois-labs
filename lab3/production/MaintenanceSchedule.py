"""
График обслуживания - план технического обслуживания
"""
from datetime import datetime, date
from typing import List


class MaintenanceSchedule:
    """График обслуживания"""

    def __init__(self, schedule_id: str):
        self.schedule_id = schedule_id
        self.machines = []
        self.engineers = []
        self.maintenance_requests = []
        self.scheduled_dates = {}  # {machine_id: [dates]}
        self.completed_maintenance = []

    def add_machine(self, machine):
        """Добавить станок в график"""
        self.machines.append(machine)
        machine.set_maintenance_schedule(self)

    def add_engineer(self, engineer):
        """Добавить инженера"""
        self.engineers.append(engineer)

    def schedule_maintenance(self, machine, maintenance_date: date):
        """Запланировать обслуживание"""
        if machine.machine_id not in self.scheduled_dates:
            self.scheduled_dates[machine.machine_id] = []
        self.scheduled_dates[machine.machine_id].append(maintenance_date)
        return {'machine': machine.name, 'scheduled_for': maintenance_date}

    def add_maintenance_request(self, request):
        """Добавить заявку на обслуживание"""
        self.maintenance_requests.append(request)

    def complete_maintenance(self, machine, engineer):
        """Отметить выполнение обслуживания"""
        record = {
            'machine': machine,
            'engineer': engineer,
            'completed_at': datetime.now()
        }
        self.completed_maintenance.append(record)
        return record

    def get_next_maintenance_date(self, machine):
        """Получить следующую дату обслуживания"""
        dates = self.scheduled_dates.get(machine.machine_id, [])
        future_dates = [d for d in dates if d >= date.today()]
        return min(future_dates) if future_dates else None

    def get_overdue_maintenance(self):
        """Получить просроченные обслуживания"""
        overdue = []
        for machine_id, dates in self.scheduled_dates.items():
            past_dates = [d for d in dates if d < date.today()]
            if past_dates:
                machine = next((m for m in self.machines if m.machine_id == machine_id), None)
                if machine:
                    overdue.append({'machine': machine, 'overdue_dates': past_dates})
        return overdue

    def __repr__(self):
        return f"MaintenanceSchedule(id='{self.schedule_id}', machines={len(self.machines)})"
