"""
Модуль финансов
"""
from .finance_department import FinanceDepartment
from .payment import Payment
from .invoice import Invoice
from .budget import Budget
from .expense import Expense

__all__ = [
    'FinanceDepartment',
    'Payment',
    'Invoice',
    'Budget',
    'Expense'
]
