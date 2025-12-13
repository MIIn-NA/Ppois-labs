"""
Работник - базовый класс для всех сотрудников
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class Employee:
    """Базовый класс для всех сотрудников"""

    def __init__(self, name: str, employee_id: str, salary: float):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.base_salary = salary
        self.department = None
        self.shift = None
        self.work_schedule = None
        self.hire_date = datetime.now()
        self.is_active = True
        self.position = "Employee"
        self.vacation_days_total = 28
        self.vacation_days_used = 0
        self.sick_days_used = 0
        self.performance_reviews = []
        self.attendance_record = []
        self.warnings = []
        self.certifications = []
        self.last_review_date = None

    def assign_to_department(self, department):
        """
        Назначить в отдел с валидацией

        Проверяет активность сотрудника и обновляет статистику отдела
        """
        if not self.is_active:
            raise RuntimeError(f"Cannot assign inactive employee {self.name}")

        # Если уже назначен в другой отдел, переводим
        if self.department is not None:
            print(f"Warning: {self.name} is being transferred from {self.department.name}")
            self.department.remove_employee(self)

        self.department = department
        department.add_employee(self)

        print(f"Employee {self.name} assigned to department '{department.name}'")
        return department

    def assign_shift(self, shift):
        """
        Назначить смену с проверкой совместимости

        Проверяет доступность и конфликты графика
        """
        if not self.is_active:
            raise RuntimeError("Cannot assign shift to inactive employee")

        # Проверка совместимости с графиком работы
        if self.work_schedule and hasattr(self.work_schedule, 'allowed_shifts'):
            if shift not in self.work_schedule.allowed_shifts:
                raise ValueError(f"Shift '{shift.name}' is not compatible with employee's work schedule")

        # Удаление из предыдущей смены
        if self.shift is not None:
            self.shift.remove_worker(self)

        self.shift = shift
        print(f"Employee {self.name} assigned to shift '{shift.name}'")

        return shift

    def set_work_schedule(self, schedule):
        """Установить график работы"""
        self.work_schedule = schedule
        print(f"Work schedule set for {self.name}: {schedule}")
        return schedule

    def increase_salary(self, amount: float, reason: str = "Merit increase"):
        """
        Увеличить зарплату с валидацией и логированием

        Проверяет корректность суммы и записывает причину изменения
        """
        if amount <= 0:
            raise ValueError("Salary increase amount must be positive")

        if amount > self.salary * 0.5:
            print(f"Warning: Large salary increase ({amount}) for {self.name}. Requires approval.")

        old_salary = self.salary
        self.salary += amount

        # Логирование изменения
        change_record = {
            'date': datetime.now(),
            'old_salary': old_salary,
            'new_salary': self.salary,
            'increase': amount,
            'reason': reason
        }

        print(f"Salary increased for {self.name}: {old_salary:.2f} -> {self.salary:.2f} ({reason})")

        return change_record

    def request_vacation(self, days: int, start_date: datetime):
        """
        Запрос отпуска с проверкой доступных дней

        Валидирует количество дней и доступность
        """
        if days <= 0:
            raise ValueError("Vacation days must be positive")

        available_days = self.vacation_days_total - self.vacation_days_used

        if days > available_days:
            raise ValueError(
                f"Insufficient vacation days. Requested: {days}, Available: {available_days}"
            )

        # Проверка минимального срока уведомления (14 дней)
        if start_date < datetime.now() + timedelta(days=14):
            print(f"Warning: Vacation request for {self.name} has less than 14 days notice")

        vacation_request = {
            'employee': self.name,
            'start_date': start_date,
            'end_date': start_date + timedelta(days=days),
            'days': days,
            'status': 'pending',
            'requested_at': datetime.now()
        }

        print(f"Vacation requested for {self.name}: {days} days starting {start_date.date()}")

        return vacation_request

    def approve_vacation(self, vacation_request: Dict):
        """Утвердить отпуск и обновить статистику"""
        days = vacation_request['days']
        self.vacation_days_used += days
        vacation_request['status'] = 'approved'

        print(f"Vacation approved for {self.name}: {days} days")
        print(f"Remaining vacation days: {self.vacation_days_total - self.vacation_days_used}")

        return vacation_request

    def record_sick_day(self, date: datetime, has_medical_note: bool = False):
        """
        Записать больничный день

        Отслеживает использование больничных и требования к документации
        """
        self.sick_days_used += 1

        sick_record = {
            'date': date,
            'has_medical_note': has_medical_note,
            'recorded_at': datetime.now()
        }

        # Предупреждение при превышении порога
        if self.sick_days_used > 10 and not has_medical_note:
            print(f"Warning: {self.name} has {self.sick_days_used} sick days without medical notes")

        print(f"Sick day recorded for {self.name} on {date.date()}")

        return sick_record

    def add_performance_review(self, rating: float, comments: str, reviewer: str):
        """
        Добавить отзыв о производительности

        Отслеживает рейтинги и может влиять на зарплату
        """
        if not 0 <= rating <= 5:
            raise ValueError("Performance rating must be between 0 and 5")

        review = {
            'date': datetime.now(),
            'rating': rating,
            'comments': comments,
            'reviewer': reviewer
        }

        self.performance_reviews.append(review)
        self.last_review_date = datetime.now()

        # Автоматическая корректировка зарплаты при отличной работе
        if rating >= 4.5:
            increase = self.base_salary * 0.05  # 5% повышение
            print(f"Excellent performance! Automatic salary increase recommended: {increase:.2f}")
        elif rating < 2.0:
            print(f"Warning: Low performance rating for {self.name}. Action required.")

        print(f"Performance review added for {self.name}: {rating}/5.0")

        return review

    def add_warning(self, reason: str, severity: str = "low"):
        """
        Добавить предупреждение сотруднику

        Отслеживает дисциплинарные меры
        """
        if severity not in ["low", "medium", "high"]:
            raise ValueError("Severity must be 'low', 'medium', or 'high'")

        warning = {
            'date': datetime.now(),
            'reason': reason,
            'severity': severity
        }

        self.warnings.append(warning)

        # Автоматическая проверка на превышение лимита
        if len(self.warnings) >= 3:
            print(f"CRITICAL: {self.name} has {len(self.warnings)} warnings. Termination review required.")

        print(f"Warning issued to {self.name}: {reason} (Severity: {severity})")

        return warning

    def terminate(self, reason: str = "Voluntary resignation"):
        """
        Уволить сотрудника с полной процедурой

        Проверяет активность, записывает причину и обновляет статистику
        """
        if not self.is_active:
            print(f"Warning: {self.name} is already terminated")
            return False

        # Подготовка к увольнению
        termination_record = {
            'employee': self.name,
            'employee_id': self.employee_id,
            'termination_date': datetime.now(),
            'hire_date': self.hire_date,
            'years_of_service': self.get_years_of_service(),
            'reason': reason,
            'final_salary': self.salary,
            'unused_vacation_days': self.vacation_days_total - self.vacation_days_used
        }

        # Удаление из отдела если назначен
        if self.department:
            self.department.remove_employee(self)

        # Удаление из смены
        if self.shift:
            self.shift.remove_worker(self)

        self.is_active = False

        print(f"Employee {self.name} terminated. Reason: {reason}")
        print(f"Years of service: {termination_record['years_of_service']:.2f}")

        return termination_record

    def get_years_of_service(self):
        """Получить стаж работы в годах"""
        delta = datetime.now() - self.hire_date
        return round(delta.days / 365.25, 2)

    def get_average_performance_rating(self):
        """Получить среднюю оценку производительности"""
        if not self.performance_reviews:
            return 0.0

        total = sum(review['rating'] for review in self.performance_reviews)
        return round(total / len(self.performance_reviews), 2)

    def get_employee_summary(self) -> Dict:
        """
        Получить полную сводку о сотруднике

        Возвращает детальную информацию для HR отчетов
        """
        summary = {
            'name': self.name,
            'employee_id': self.employee_id,
            'position': self.position,
            'department': self.department.name if self.department else None,
            'is_active': self.is_active,
            'hire_date': self.hire_date.date(),
            'years_of_service': self.get_years_of_service(),
            'salary': self.salary,
            'vacation_days_remaining': self.vacation_days_total - self.vacation_days_used,
            'sick_days_used': self.sick_days_used,
            'average_performance': self.get_average_performance_rating(),
            'total_reviews': len(self.performance_reviews),
            'warnings_count': len(self.warnings),
            'certifications_count': len(self.certifications),
            'last_review': self.last_review_date.date() if self.last_review_date else None
        }

        return summary

    def reset_annual_stats(self):
        """Сбросить годовую статистику (для нового года)"""
        self.vacation_days_used = 0
        self.sick_days_used = 0
        self.warnings = []  # Можно оставить для истории, но обычно сбрасывают

        print(f"Annual stats reset for {self.name}")
        print(f"Vacation days restored: {self.vacation_days_total}")

    def __repr__(self):
        return f"Employee(name='{self.name}', id='{self.employee_id}', position='{self.position}')"
