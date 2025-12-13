"""
Платеж - финансовая транзакция
"""
from datetime import datetime


class Payment:
    """Платеж"""

    def __init__(self, payment_id: str, amount: float, payment_type: str):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_type = payment_type  # incoming, outgoing
        self.order = None
        self.purchase_order = None
        self.customer = None
        self.supplier = None
        self.invoice = None
        self.payment_method = "bank_transfer"  # bank_transfer, cash, credit_card
        self.payment_date = datetime.now()
        self.status = "pending"  # pending, completed, failed, refunded

    def set_order(self, order):
        """Установить заказ клиента"""
        self.order = order
        order.add_payment(self)

    def set_purchase_order(self, purchase_order):
        """Установить заказ на закупку"""
        self.purchase_order = purchase_order
        purchase_order.add_payment(self)

    def set_customer(self, customer):
        """Установить клиента"""
        self.customer = customer
        customer.add_payment({'payment_id': self.payment_id, 'amount': self.amount})

    def set_supplier(self, supplier):
        """Установить поставщика"""
        self.supplier = supplier
        supplier.add_payment({'payment_id': self.payment_id, 'amount': self.amount})

    def set_invoice(self, invoice):
        """Установить счет"""
        self.invoice = invoice

    def set_payment_method(self, method: str):
        """Установить способ оплаты"""
        self.payment_method = method

    def complete(self):
        """Завершить платеж"""
        self.status = "completed"
        return {'payment': self.payment_id, 'completed_at': datetime.now()}

    def fail(self, reason: str):
        """Провалить платеж"""
        self.status = "failed"
        return {'payment': self.payment_id, 'failed_at': datetime.now(), 'reason': reason}

    def refund(self):
        """Возврат платежа"""
        self.status = "refunded"
        return {'payment': self.payment_id, 'refunded_at': datetime.now()}

    def is_completed(self):
        """Проверить, завершен ли платеж"""
        return self.status == "completed"

    def get_details(self):
        """Получить детали платежа"""
        return {
            'payment_id': self.payment_id,
            'amount': self.amount,
            'type': self.payment_type,
            'method': self.payment_method,
            'status': self.status,
            'date': self.payment_date
        }

    def __repr__(self):
        return f"Payment(id='{self.payment_id}', amount={self.amount}, type='{self.payment_type}', status='{self.status}')"
