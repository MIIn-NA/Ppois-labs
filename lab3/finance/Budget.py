"""
Бюджет - финансовый план
"""
from datetime import datetime


class Budget:
    """Бюджет"""

    def __init__(self, budget_id: str, period_start: datetime, period_end: datetime, allocated_amount: float):
        self.budget_id = budget_id
        self.period_start = period_start
        self.period_end = period_end
        self.allocated_amount = allocated_amount
        self.department = None
        self.finance_department = None
        self.expenses = []
        self.spent_amount = 0.0
        self.status = "active"  # active, depleted, expired

    def set_department(self, department):
        """Установить отдел"""
        self.department = department
        department.set_budget(self)

    def set_finance_department(self, finance_dept):
        """Установить финансовый отдел"""
        self.finance_department = finance_dept
        finance_dept.add_budget(self)

    def add_expense(self, expense):
        """Добавить расход"""
        self.expenses.append(expense)
        if hasattr(expense, 'amount'):
            self.spent_amount += expense.amount
            if self.spent_amount >= self.allocated_amount:
                self.status = "depleted"

    def get_remaining_amount(self):
        """Получить оставшуюся сумму"""
        return max(0, self.allocated_amount - self.spent_amount)

    def get_utilization_percentage(self):
        """Получить процент использования"""
        if self.allocated_amount == 0:
            return 0
        return (self.spent_amount / self.allocated_amount) * 100

    def is_depleted(self):
        """Проверить, исчерпан ли бюджет"""
        return self.spent_amount >= self.allocated_amount

    def check_expiration(self):
        """Проверить истечение срока"""
        if datetime.now() > self.period_end and self.status == "active":
            self.status = "expired"
            return True
        return False

    def increase_allocation(self, amount: float):
        """Увеличить выделенную сумму"""
        self.allocated_amount += amount
        if self.status == "depleted" and self.spent_amount < self.allocated_amount:
            self.status = "active"

    def __repr__(self):
        return f"Budget(id='{self.budget_id}', allocated={self.allocated_amount}, spent={self.spent_amount}, status='{self.status}')"
