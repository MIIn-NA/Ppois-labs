"""
Модуль персонала
"""
from .employee import Employee
from .worker import Worker
from .engineer import Engineer
from .quality_inspector import QualityInspector
from .accountant import Accountant
from .shift import Shift
from .work_schedule import WorkSchedule

__all__ = [
    'Employee',
    'Worker',
    'Engineer',
    'QualityInspector',
    'Accountant',
    'Shift',
    'WorkSchedule'
]
