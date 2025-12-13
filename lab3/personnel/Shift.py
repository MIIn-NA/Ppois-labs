"""
Смена - рабочая смена
"""
from datetime import datetime, time, timedelta
from typing import List, Dict


class Shift:
    """Рабочая смена"""

    def __init__(self, shift_id: str, name: str, start_time: time, end_time: time):
        self.shift_id = shift_id
        self.name = name  # Morning, Day, Night
        self.start_time = start_time
        self.end_time = end_time
        self.workers = []
        self.production_lines = []
        self.work_schedule = None
        self.is_active = False
        self.shift_start_datetime = None
        self.shift_end_datetime = None
        self.max_worker_capacity = 50
        self.attendance_records = []
        self.production_records = []
        self.incidents = []

    def add_worker(self, worker):
        """
        Добавить рабочего в смену с проверкой емкости

        Валидирует доступность мест в смене
        """
        if len(self.workers) >= self.max_worker_capacity:
            raise ValueError(
                f"Shift {self.name} has reached maximum capacity ({self.max_worker_capacity} workers)"
            )

        # Проверка дубликатов
        if worker in self.workers:
            print(f"Warning: Worker {worker.name} is already assigned to shift {self.name}")
            return worker

        # Проверка активности рабочего
        if hasattr(worker, 'is_active') and not worker.is_active:
            raise RuntimeError(f"Cannot assign inactive worker {worker.name} to shift")

        self.workers.append(worker)
        worker.assign_shift(self)

        print(f"Worker {worker.name} added to shift '{self.name}'")
        print(f"Current shift occupancy: {len(self.workers)}/{self.max_worker_capacity}")

        return worker

    def remove_worker(self, worker):
        """
        Удалить рабочего из смены

        Обновляет список и статистику
        """
        if worker in self.workers:
            self.workers.remove(worker)
            print(f"Worker {worker.name} removed from shift '{self.name}'")
            return True
        else:
            print(f"Warning: Worker {worker.name} is not assigned to this shift")
            return False

    def add_production_line(self, production_line):
        """
        Добавить производственную линию в смену

        Проверяет уникальность линии
        """
        if production_line in self.production_lines:
            print(f"Warning: Production line already assigned to shift {self.name}")
            return production_line

        self.production_lines.append(production_line)

        print(f"Production line '{production_line.name if hasattr(production_line, 'name') else production_line}' assigned to shift '{self.name}'")

        return production_line

    def set_work_schedule(self, schedule):
        """Установить график работы"""
        self.work_schedule = schedule
        print(f"Work schedule set for shift '{self.name}'")
        return schedule

    def record_attendance(self, worker, status: str = "present"):
        """
        Записать посещаемость рабочего

        Отслеживает явку, опоздания и отсутствия
        """
        if status not in ["present", "late", "absent", "sick"]:
            raise ValueError("Status must be 'present', 'late', 'absent', or 'sick'")

        if worker not in self.workers:
            raise ValueError(f"Worker {worker.name} is not assigned to this shift")

        attendance = {
            'worker': worker.name,
            'shift_date': datetime.now().date(),
            'shift_id': self.shift_id,
            'status': status,
            'recorded_at': datetime.now()
        }

        self.attendance_records.append(attendance)

        if status == "absent":
            print(f"Warning: Worker {worker.name} is absent from shift '{self.name}'")
        elif status == "late":
            print(f"Worker {worker.name} arrived late to shift '{self.name}'")

        return attendance

    def get_attendance_rate(self) -> float:
        """
        Рассчитать уровень посещаемости смены

        Возвращает процент присутствующих рабочих
        """
        if not self.attendance_records:
            return 100.0

        present_count = sum(1 for record in self.attendance_records
                          if record['status'] in ['present', 'late'])
        total_records = len(self.attendance_records)

        return round((present_count / total_records) * 100, 2)

    def start_shift(self):
        """
        Начать смену с проверками готовности

        Валидирует наличие рабочих и производственных линий
        """
        if self.is_active:
            print(f"Warning: Shift '{self.name}' is already active")
            return False

        # Проверка минимального количества рабочих
        if len(self.workers) == 0:
            raise RuntimeError(f"Cannot start shift '{self.name}' with no workers assigned")

        # Проверка наличия производственных линий
        if len(self.production_lines) == 0:
            print(f"Warning: Starting shift '{self.name}' with no production lines assigned")

        self.is_active = True
        self.shift_start_datetime = datetime.now()

        # Автоматическая регистрация посещаемости для всех рабочих
        for worker in self.workers:
            if hasattr(worker, 'is_active') and worker.is_active:
                self.record_attendance(worker, "present")

        result = {
            'shift': self.name,
            'shift_id': self.shift_id,
            'started_at': self.shift_start_datetime,
            'workers_count': len(self.workers),
            'production_lines_count': len(self.production_lines)
        }

        print(f"Shift '{self.name}' started at {self.shift_start_datetime.time()}")
        print(f"Workers: {len(self.workers)} | Production lines: {len(self.production_lines)}")

        return result

    def end_shift(self):
        """
        Закончить смену с подведением итогов

        Рассчитывает производительность и генерирует отчет
        """
        if not self.is_active:
            print(f"Warning: Shift '{self.name}' is not active")
            return False

        self.is_active = False
        self.shift_end_datetime = datetime.now()

        # Расчет продолжительности смены
        if self.shift_start_datetime:
            actual_duration = (self.shift_end_datetime - self.shift_start_datetime).total_seconds() / 3600
        else:
            actual_duration = 0

        # Сбор статистики по производству
        total_production = self._calculate_shift_production()

        result = {
            'shift': self.name,
            'shift_id': self.shift_id,
            'started_at': self.shift_start_datetime,
            'ended_at': self.shift_end_datetime,
            'actual_duration_hours': round(actual_duration, 2),
            'planned_duration_hours': self.get_duration_hours(),
            'workers_count': len(self.workers),
            'attendance_rate': self.get_attendance_rate(),
            'total_production': total_production,
            'incidents_count': len(self.incidents)
        }

        print(f"Shift '{self.name}' ended at {self.shift_end_datetime.time()}")
        print(f"Duration: {actual_duration:.2f}h | Attendance: {result['attendance_rate']:.1f}%")

        return result

    def _calculate_shift_production(self) -> int:
        """Рассчитать общий объем производства за смену"""
        total = 0

        for line in self.production_lines:
            if hasattr(line, 'production_volume'):
                total += line.production_volume

        return total

    def record_incident(self, description: str, severity: str = "low"):
        """
        Записать инцидент во время смены

        Отслеживает проблемы безопасности и производственные сбои
        """
        if severity not in ["low", "medium", "high", "critical"]:
            raise ValueError("Severity must be 'low', 'medium', 'high', or 'critical'")

        incident = {
            'incident_id': f"INC-{len(self.incidents) + 1:04d}",
            'shift_id': self.shift_id,
            'shift_name': self.name,
            'description': description,
            'severity': severity,
            'timestamp': datetime.now(),
            'requires_investigation': severity in ["high", "critical"]
        }

        self.incidents.append(incident)

        if severity == "critical":
            print(f"CRITICAL INCIDENT during shift '{self.name}': {description}")
        else:
            print(f"Incident recorded (Severity: {severity}): {description}")

        return incident

    def get_worker_count(self):
        """Получить количество рабочих"""
        return len(self.workers)

    def get_duration_hours(self):
        """
        Получить плановую продолжительность смены в часах

        Учитывает переход через полночь для ночных смен
        """
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)

        # Если смена идет через полночь
        if end <= start:
            end = end + timedelta(days=1)

        delta = end - start
        return round(delta.total_seconds() / 3600, 2)

    def get_shift_statistics(self) -> Dict:
        """
        Получить полную статистику смены

        Возвращает детальную информацию о работе смены
        """
        stats = {
            'shift_id': self.shift_id,
            'shift_name': self.name,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'duration_hours': self.get_duration_hours(),
            'is_active': self.is_active,
            'workers_assigned': len(self.workers),
            'max_capacity': self.max_worker_capacity,
            'occupancy_rate': round((len(self.workers) / self.max_worker_capacity) * 100, 2),
            'production_lines': len(self.production_lines),
            'attendance_rate': self.get_attendance_rate(),
            'total_incidents': len(self.incidents),
            'critical_incidents': len([i for i in self.incidents if i['severity'] == 'critical'])
        }

        return stats

    def handover_to_next_shift(self, next_shift, notes: str = ""):
        """
        Передача смены следующей смене

        Создает отчет о передаче с ключевой информацией
        """
        if self.is_active:
            print(f"Warning: Attempting handover while shift '{self.name}' is still active")

        handover = {
            'from_shift': self.name,
            'to_shift': next_shift.name if hasattr(next_shift, 'name') else str(next_shift),
            'timestamp': datetime.now(),
            'production_status': self._calculate_shift_production(),
            'active_incidents': [i for i in self.incidents if i['requires_investigation']],
            'notes': notes,
            'workers_on_duty': len(self.workers)
        }

        print(f"Shift handover: {self.name} -> {handover['to_shift']}")
        print(f"Active incidents: {len(handover['active_incidents'])}")

        if handover['active_incidents']:
            print("WARNING: Active incidents require attention:")
            for incident in handover['active_incidents']:
                print(f"  - {incident['description']} (Severity: {incident['severity']})")

        return handover

    def __repr__(self):
        return f"Shift(name='{self.name}', workers={len(self.workers)}, active={self.is_active})"
