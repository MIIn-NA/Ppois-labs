"""
Счет/накладная - документ на оплату
"""
from datetime import datetime, timedelta


class Invoice:
    """Счет/накладная"""

    def __init__(self, invoice_id: str, amount: float, due_date: datetime):
        self.invoice_id = invoice_id
        self.amount = amount
        self.due_date = due_date
        self.order = None
        self.payment = None
        self.customer = None
        self.accountant = None
        self.issue_date = datetime.now()
        self.paid_date = None
        self.status = "unpaid"  # unpaid, paid, overdue, cancelled

    def set_order(self, order):
        """Установить заказ"""
        self.order = order

    def set_payment(self, payment):
        """Установить платеж"""
        self.payment = payment
        payment.set_invoice(self)

    def set_customer(self, customer):
        """Установить клиента"""
        self.customer = customer

    def set_accountant(self, accountant):
        """Установить бухгалтера"""
        self.accountant = accountant

    def mark_paid(self):
        """Отметить оплаченным"""
        self.status = "paid"
        self.paid_date = datetime.now()
        return {'invoice': self.invoice_id, 'paid_at': self.paid_date}

    def mark_overdue(self):
        """Отметить просроченным"""
        self.status = "overdue"
        return {'invoice': self.invoice_id, 'overdue_at': datetime.now()}

    def cancel(self):
        """Отменить счет"""
        self.status = "cancelled"
        return {'invoice': self.invoice_id, 'cancelled_at': datetime.now()}

    def check_overdue(self):
        """Проверить просрочку"""
        if self.status == "unpaid" and datetime.now() > self.due_date:
            self.mark_overdue()
            return True
        return False

    def get_days_until_due(self):
        """Получить дни до оплаты"""
        if self.status == "unpaid":
            delta = self.due_date - datetime.now()
            return delta.days
        return 0

    def get_days_overdue(self):
        """Получить дни просрочки"""
        if self.status == "overdue":
            delta = datetime.now() - self.due_date
            return delta.days
        return 0

    def is_paid(self):
        """Проверить, оплачен ли счет"""
        return self.status == "paid"

    def __repr__(self):
        return f"Invoice(id='{self.invoice_id}', amount={self.amount}, status='{self.status}')"
