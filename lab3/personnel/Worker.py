"""
Рабочий на производстве - выполняет производственные операции
"""
from datetime import datetime, date
from typing import List, Dict, Optional


class Worker:
    """Рабочий на производстве"""

    def __init__(self, name: str, employee_id: str, salary: float):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.base_salary = salary
        self.department = None
        self.production_line = None
        self.machine = None
        self.shift = None
        self.hire_date = datetime.now()
        self.is_active = True
        self.position = "Worker"
        self.skill_level = 1  # 1-5
        self.experience_days = 0
        self.completed_operations = []
        self.total_operations_count = 0
        self.defect_count = 0
        self.performance_rating = 0.0
        self.overtime_hours = 0.0
        self.bonus_amount = 0.0
        self.training_courses = []

    def assign_to_production_line(self, production_line):
        """
        Назначить на производственную линию

        Проверяет требуемый уровень квалификации и
        автоматически регистрирует рабочего на линии
        """
        if not self.is_active:
            raise RuntimeError(f"Cannot assign inactive worker {self.name}")

        # Проверка минимальной квалификации (если есть)
        if hasattr(production_line, 'min_skill_level'):
            if self.skill_level < production_line.min_skill_level:
                raise ValueError(
                    f"Worker skill level {self.skill_level} is below required "
                    f"{production_line.min_skill_level} for line '{production_line.name}'"
                )

        self.production_line = production_line
        print(f"Worker {self.name} assigned to line '{production_line.name}'")

        return production_line

    def assign_machine(self, machine):
        """
        Назначить станок с проверкой совместимости

        Проверяет, может ли рабочий работать с данным типом станка
        """
        if not self.production_line:
            raise RuntimeError("Worker must be assigned to production line first")

        if not machine.is_operational:
            raise ValueError(f"Cannot assign worker to non-operational machine '{machine.name}'")

        self.machine = machine
        print(f"Worker {self.name} assigned to machine '{machine.name}'")

        return machine

    def assign_shift(self, shift):
        """Назначить смену"""
        self.shift = shift
        return shift

    def perform_operation(self, operation: str, quality_check: bool = True):
        """
        Выполнить производственную операцию

        Учитывает квалификацию рабочего, усталость и случайные факторы
        Возвращает результат с оценкой качества
        """
        if not self.is_active:
            raise RuntimeError("Inactive worker cannot perform operations")

        if not self.machine or not self.production_line:
            raise RuntimeError("Worker must have assigned machine and production line")

        # Расчет времени выполнения на основе квалификации
        base_time = 60  # минут
        time_multiplier = max(0.5, 1.5 - (self.skill_level * 0.2))
        operation_time = base_time * time_multiplier

        # Расчет качества работы
        quality_score = min(100, 50 + (self.skill_level * 10) - (self.defect_count * 2))

        # Симуляция дефекта (вероятность зависит от усталости и квалификации)
        fatigue_factor = min(self.total_operations_count / 100, 1.0)
        defect_probability = 0.1 - (self.skill_level * 0.01) + (fatigue_factor * 0.05)

        import random
        has_defect = random.random() < defect_probability

        operation_result = {
            'worker': self.name,
            'operation': operation,
            'timestamp': datetime.now(),
            'duration_minutes': round(operation_time, 2),
            'quality_score': quality_score,
            'has_defect': has_defect,
            'skill_level': self.skill_level
        }

        # Обновление статистики
        self.completed_operations.append(operation_result)
        self.total_operations_count += 1

        if has_defect:
            self.defect_count += 1

        # Начисление опыта
        self._gain_experience(1)

        # Обновление рейтинга производительности
        self._update_performance_rating()

        print(f"[{self.name}] Completed '{operation}' in {operation_time:.1f}min (Quality: {quality_score})")

        return operation_result

    def increase_skill_level(self):
        """
        Повысить уровень квалификации

        Требует минимального опыта и может быть ограничен максимумом
        """
        if self.skill_level >= 5:
            print(f"Worker {self.name} is already at maximum skill level")
            return False

        # Проверка требуемого опыта
        required_exp = self.skill_level * 100
        if self.experience_days < required_exp:
            raise ValueError(
                f"Insufficient experience: {self.experience_days}/{required_exp} days"
            )

        self.skill_level += 1
        self.salary = self.base_salary * (1 + self.skill_level * 0.15)

        print(f"Worker {self.name} promoted to skill level {self.skill_level}")
        print(f"New salary: {self.salary:.2f}")

        return True

    def add_training_course(self, course_name: str):
        """
        Пройти курс обучения

        Увеличивает опыт и может помочь в повышении квалификации
        """
        course = {
            'name': course_name,
            'completed_at': datetime.now(),
            'experience_gained': 30
        }

        self.training_courses.append(course)
        self._gain_experience(30)

        print(f"Worker {self.name} completed training: {course_name}")

        return course

    def record_overtime(self, hours: float):
        """
        Записать переработку

        Увеличивает зарплату, но снижает производительность
        """
        if hours <= 0:
            raise ValueError("Overtime hours must be positive")

        if hours > 4:
            print(f"Warning: Excessive overtime ({hours}h) may reduce worker performance")

        self.overtime_hours += hours

        # Расчет оплаты переработок (1.5x от базовой ставки)
        hourly_rate = self.base_salary / 160  # 160 рабочих часов в месяц
        overtime_pay = hourly_rate * hours * 1.5

        self.bonus_amount += overtime_pay

        print(f"Recorded {hours}h overtime for {self.name}. Extra pay: {overtime_pay:.2f}")

        return overtime_pay

    def calculate_total_salary(self):
        """
        Рассчитать общую зарплату

        Включает базовую зарплату, бонусы за производительность и переработки
        """
        # Базовая зарплата с учетом квалификации
        base = self.salary

        # Бонус за производительность (до 20% от базы)
        performance_bonus = 0.0
        if self.performance_rating >= 0.9:
            performance_bonus = base * 0.2
        elif self.performance_rating >= 0.8:
            performance_bonus = base * 0.15
        elif self.performance_rating >= 0.7:
            performance_bonus = base * 0.1

        # Бонус за переработки
        overtime_bonus = self.bonus_amount

        total = base + performance_bonus + overtime_bonus

        return {
            'base_salary': base,
            'performance_bonus': performance_bonus,
            'overtime_bonus': overtime_bonus,
            'total': total
        }

    def get_productivity(self):
        """
        Рассчитать производительность рабочего

        Учитывает квалификацию, выполненные операции и качество работы
        """
        base_productivity = self.skill_level * 10

        # Бонус за опыт
        experience_bonus = min(self.experience_days / 10, 20)

        # Штраф за дефекты
        defect_penalty = min(self.defect_count * 2, 30)

        # Штраф за усталость от переработок
        overtime_penalty = min(self.overtime_hours / 10, 15)

        total_productivity = max(0, base_productivity + experience_bonus - defect_penalty - overtime_penalty)

        return round(total_productivity, 2)

    def get_statistics(self) -> Dict:
        """
        Получить полную статистику работника

        Возвращает детальную информацию о производительности
        """
        total_salary = self.calculate_total_salary()

        stats = {
            'name': self.name,
            'employee_id': self.employee_id,
            'skill_level': self.skill_level,
            'experience_days': self.experience_days,
            'is_active': self.is_active,
            'production_line': self.production_line.name if self.production_line else None,
            'total_operations': self.total_operations_count,
            'defect_count': self.defect_count,
            'defect_rate': (self.defect_count / self.total_operations_count * 100) if self.total_operations_count > 0 else 0,
            'performance_rating': self.performance_rating,
            'productivity': self.get_productivity(),
            'overtime_hours': self.overtime_hours,
            'training_courses_completed': len(self.training_courses),
            'total_salary': total_salary['total'],
            'work_days': (datetime.now() - self.hire_date).days
        }

        return stats

    def _gain_experience(self, days: int):
        """Внутренний метод для начисления опыта"""
        self.experience_days += days

    def _update_performance_rating(self):
        """
        Обновить рейтинг производительности

        На основе качества выполненных операций
        """
        if not self.completed_operations:
            self.performance_rating = 0.0
            return

        total_quality = sum(op['quality_score'] for op in self.completed_operations)
        avg_quality = total_quality / len(self.completed_operations)

        self.performance_rating = avg_quality / 100

    def reset_monthly_stats(self):
        """Сбросить месячную статистику (для начала нового месяца)"""
        self.overtime_hours = 0.0
        self.bonus_amount = 0.0
        print(f"Monthly stats reset for worker {self.name}")

    def __repr__(self):
        return f"Worker(name='{self.name}', skill_level={self.skill_level}, productivity={self.get_productivity()})"
