"""
Тесты для класса Director
"""
import pytest
from factory.management.director import Director
from factory.management.factory import Factory
from factory.management.department import Department
from factory.management.production_plan import ProductionPlan
from datetime import datetime


class TestDirector:
    """Тесты для класса Director"""

    def test_director_creation(self):
        """Тест создания директора"""
        director = Director("John Smith", "DIR-001")
        assert director.name == "John Smith"
        assert director.employee_id == "DIR-001"
        assert len(director.departments) == 0
        assert len(director.production_plans) == 0

    def test_assign_to_factory(self):
        """Тест назначения на фабрику"""
        director = Director("John Smith", "DIR-001")
        factory = Factory("Test Factory", "Moscow")
        director.assign_to_factory(factory)
        assert director.factory == factory

    def test_add_department(self):
        """Тест добавления отдела"""
        director = Director("John Smith", "DIR-001")
        dept = Department("HR", "DEPT-001")
        director.add_department(dept)
        assert len(director.departments) == 1
        assert dept in director.departments

    def test_create_production_plan(self):
        """Тест создания плана производства"""
        director = Director("John Smith", "DIR-001")
        plan = ProductionPlan("PLAN-001", datetime.now(), datetime.now())
        result = director.create_production_plan(plan)
        assert result == plan
        assert len(director.production_plans) == 1
        assert plan in director.production_plans

    def test_review_financial_report(self):
        """Тест проверки финансового отчета"""
        director = Director("John Smith", "DIR-001")
        report = {"report_id": "FIN-001", "revenue": 1000000}
        director.review_financial_report(report)
        assert len(director.financial_reports) == 1
        assert report in director.financial_reports

    def test_make_strategic_decision(self):
        """Тест принятия стратегического решения"""
        director = Director("John Smith", "DIR-001")
        result = director.make_strategic_decision("Expand production capacity")
        assert result['decision'] == "Expand production capacity"
        assert result['director'] == "John Smith"
        assert 'timestamp' in result

    def test_get_departments_count(self):
        """Тест получения количества отделов"""
        director = Director("John Smith", "DIR-001")
        assert director.get_departments_count() == 0
        director.add_department(Department("HR", "DEPT-001"))
        director.add_department(Department("IT", "DEPT-002"))
        assert director.get_departments_count() == 2

    def test_repr(self):
        """Тест строкового представления"""
        director = Director("John Smith", "DIR-001")
        assert "John Smith" in repr(director)
        assert "DIR-001" in repr(director)
