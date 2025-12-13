"""
Расход - статья расходов
"""
from datetime import datetime


class Expense:
    """Расход"""

    def __init__(self, expense_id: str, amount: float, category: str, description: str):
        self.expense_id = expense_id
        self.amount = amount
        self.category = category  # salaries, materials, utilities, maintenance, other
        self.description = description
        self.budget = None
        self.payment = None
        self.department = None
        self.expense_date = datetime.now()
        self.approved_by = None
        self.status = "pending"  # pending, approved, rejected, paid

    def set_budget(self, budget):
        """Установить бюджет"""
        self.budget = budget
        budget.add_expense(self)

    def set_payment(self, payment):
        """Установить платеж"""
        self.payment = payment

    def set_department(self, department):
        """Установить отдел"""
        self.department = department

    def approve(self, approver: str):
        """Утвердить расход"""
        self.status = "approved"
        self.approved_by = approver
        return {'expense': self.expense_id, 'approved_at': datetime.now(), 'approved_by': approver}

    def reject(self, reason: str):
        """Отклонить расход"""
        self.status = "rejected"
        return {'expense': self.expense_id, 'rejected_at': datetime.now(), 'reason': reason}

    def mark_paid(self):
        """Отметить оплаченным"""
        self.status = "paid"
        return {'expense': self.expense_id, 'paid_at': datetime.now()}

    def is_approved(self):
        """Проверить, утвержден ли расход"""
        return self.status == "approved"

    def is_paid(self):
        """Проверить, оплачен ли расход"""
        return self.status == "paid"

    def get_details(self):
        """Получить детали расхода"""
        return {
            'expense_id': self.expense_id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'status': self.status,
            'expense_date': self.expense_date,
            'approved_by': self.approved_by
        }

    def __repr__(self):
        return f"Expense(id='{self.expense_id}', amount={self.amount}, category='{self.category}', status='{self.status}')"
