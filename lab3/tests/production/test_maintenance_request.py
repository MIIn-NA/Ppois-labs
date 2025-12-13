"""Тесты для MaintenanceRequest"""
import pytest
from factory.production.maintenance_request import MaintenanceRequest

class TestMaintenanceRequest:
    def test_creation(self):
        r = MaintenanceRequest("REQ001", "Oil change", "medium")
        assert r.request_id == "REQ001"
        assert r.priority == "medium"
        assert r.status == "pending"
    
    def test_start_work_and_complete(self):
        r = MaintenanceRequest("REQ001", "Oil change")
        r.start_work()
        assert r.status == "in_progress"
        r.complete()
        assert r.status == "completed"
    
    def test_escalate_priority(self):
        r = MaintenanceRequest("REQ001", "Oil change", "low")
        r.escalate_priority()
        assert r.priority == "medium"
