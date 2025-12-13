"""
Договор - контракт с поставщиком/клиентом
"""
from datetime import datetime
from typing import List


class Contract:
    """Договор"""

    def __init__(self, contract_id: str, start_date: datetime, end_date: datetime):
        self.contract_id = contract_id
        self.start_date = start_date
        self.end_date = end_date
        self.supplier = None
        self.customer = None
        self.payments = []
        self.contract_terms = []
        self.total_value = 0.0
        self.status = "draft"  # draft, active, expired, terminated
        self.signed_at = None

    def set_supplier(self, supplier):
        """Установить поставщика"""
        self.supplier = supplier
        supplier.add_contract(self)

    def set_customer(self, customer):
        """Установить клиента"""
        self.customer = customer

    def add_payment(self, payment):
        """Добавить платеж"""
        self.payments.append(payment)

    def add_contract_term(self, term):
        """Добавить условие договора"""
        self.contract_terms.append(term)

    def set_total_value(self, value: float):
        """Установить общую стоимость"""
        self.total_value = value

    def sign(self):
        """Подписать договор"""
        self.status = "active"
        self.signed_at = datetime.now()
        return {'contract': self.contract_id, 'signed_at': self.signed_at}

    def terminate(self, reason: str):
        """Расторгнуть договор"""
        self.status = "terminated"
        return {'contract': self.contract_id, 'terminated_at': datetime.now(), 'reason': reason}

    def check_expiration(self):
        """Проверить истечение срока"""
        if datetime.now() > self.end_date and self.status == "active":
            self.status = "expired"
            return True
        return False

    def is_active(self):
        """Проверить, активен ли договор"""
        return self.status == "active" and datetime.now() <= self.end_date

    def get_remaining_days(self):
        """Получить оставшиеся дни"""
        if self.status == "active":
            delta = self.end_date - datetime.now()
            return max(0, delta.days)
        return 0

    def get_total_paid(self):
        """Получить общую оплаченную сумму"""
        return sum(p.get('amount', 0) for p in self.payments)

    def __repr__(self):
        return f"Contract(id='{self.contract_id}', status='{self.status}', value={self.total_value})"
