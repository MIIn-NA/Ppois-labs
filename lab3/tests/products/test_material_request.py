"""Тесты для MaterialRequest"""
import pytest
from factory.products.material_request import MaterialRequest

class TestMaterialRequest:
    def test_creation(self):
        r = MaterialRequest("REQ001", 100.0)
        assert r.request_id == "REQ001"
        assert r.quantity == 100.0
        assert r.status == "pending"
    
    def test_approve_fulfill(self):
        r = MaterialRequest("REQ001", 100.0)
        r.approve()
        assert r.status == "approved"
        r.fulfill()
        assert r.status == "fulfilled"
    
    def test_reject(self):
        r = MaterialRequest("REQ001", 100.0)
        r.reject("Out of stock")
        assert r.status == "rejected"
