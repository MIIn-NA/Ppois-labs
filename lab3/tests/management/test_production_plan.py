"""
Тесты для класса ProductionPlan
"""
import pytest
from datetime import datetime, timedelta
from factory.management.production_plan import ProductionPlan
from factory.management.director import Director
from factory.production.production_line import ProductionLine
from factory.products.product import Product
from factory.customers.order import Order


class TestProductionPlan:
    """Тесты для класса ProductionPlan"""

    def test_production_plan_creation(self):
        """Тест создания плана производства"""
        start = datetime.now()
        end = start + timedelta(days=30)
        plan = ProductionPlan("PLAN-001", start, end)
        assert plan.plan_id == "PLAN-001"
        assert plan.start_date == start
        assert plan.end_date == end
        assert plan.status == "planned"
        assert plan.target_volume == 0

    def test_set_director(self):
        """Тест установки директора"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        director = Director("John Smith", "DIR-001")
        plan.set_director(director)
        assert plan.director == director

    def test_add_production_line(self):
        """Тест добавления производственной линии"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        line = ProductionLine("LINE-001", "Assembly Line")
        plan.add_production_line(line)
        assert len(plan.production_lines) == 1
        assert line in plan.production_lines

    def test_add_product(self):
        """Тест добавления продукта"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        product = Product("PROD-001", "Widget", "Test product")
        plan.add_product(product)
        assert len(plan.products) == 1
        assert product in plan.products

    def test_add_order(self):
        """Тест добавления заказа"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        order = Order("ORD-001", datetime.now())
        plan.add_order(order)
        assert len(plan.orders) == 1
        assert order in plan.orders

    def test_set_target_volume(self):
        """Тест установки целевого объема"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        plan.set_target_volume(1000)
        assert plan.target_volume == 1000

    def test_update_actual_volume(self):
        """Тест обновления фактического объема"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        plan.update_actual_volume(500)
        assert plan.actual_volume == 500

    def test_start_plan(self):
        """Тест начала выполнения плана"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        plan.start_plan()
        assert plan.status == "in_progress"

    def test_complete_plan(self):
        """Тест завершения плана"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        plan.complete_plan()
        assert plan.status == "completed"

    def test_get_completion_percentage(self):
        """Тест получения процента выполнения"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        plan.set_target_volume(1000)
        plan.update_actual_volume(750)
        assert plan.get_completion_percentage() == 75.0

    def test_get_completion_percentage_zero_target(self):
        """Тест процента выполнения при нулевой цели"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        assert plan.get_completion_percentage() == 0

    def test_repr(self):
        """Тест строкового представления"""
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        assert "PLAN-001" in repr(plan)
        assert "planned" in repr(plan)
