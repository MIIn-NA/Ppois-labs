"""
Модуль клиентов и продаж
"""
from .customer import Customer
from .order import Order
from .sales_manager import SalesManager
from .sales_report import SalesReport
from .discount import Discount

__all__ = [
    'Customer',
    'Order',
    'SalesManager',
    'SalesReport',
    'Discount'
]
