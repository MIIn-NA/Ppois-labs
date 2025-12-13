"""
План производства - определяет цели и сроки
"""
from datetime import datetime
from typing import List


class ProductionPlan:
    """План производства"""

    def __init__(self, plan_id: str, start_date: datetime, end_date: datetime):
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date
        self.director = None
        self.production_lines = []
        self.products = []
        self.orders = []
        self.target_volume = 0
        self.actual_volume = 0
        self.status = "planned"  # planned, in_progress, completed, cancelled

    def set_director(self, director):
        """Установить директора"""
        self.director = director

    def add_production_line(self, production_line):
        """Добавить производственную линию"""
        self.production_lines.append(production_line)

    def add_product(self, product):
        """Добавить продукт в план"""
        self.products.append(product)

    def add_order(self, order):
        """Добавить заказ в план"""
        self.orders.append(order)

    def set_target_volume(self, volume: int):
        """Установить целевой объем"""
        self.target_volume = volume

    def update_actual_volume(self, volume: int):
        """Обновить фактический объем"""
        self.actual_volume = volume

    def start_plan(self):
        """Начать выполнение плана"""
        self.status = "in_progress"

    def complete_plan(self):
        """Завершить план"""
        self.status = "completed"

    def get_completion_percentage(self):
        """Получить процент выполнения"""
        if self.target_volume == 0:
            return 0
        return (self.actual_volume / self.target_volume) * 100

    def __repr__(self):
        return f"ProductionPlan(id='{self.plan_id}', status='{self.status}')"
