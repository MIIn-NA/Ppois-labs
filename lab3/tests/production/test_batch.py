"""Тесты для Batch"""
import pytest
from factory.production.batch import Batch

class TestBatch:
    def test_creation(self):
        b = Batch("B001", 100)
        assert b.batch_id == "B001"
        assert b.quantity == 100
        assert b.quality_status == "pending"
    
    def test_pass_quality_control(self):
        b = Batch("B001", 100)
        b.pass_quality_control()
        assert b.quality_status == "passed"
        assert b.is_quality_approved() is True
    
    def test_fail_quality_control(self):
        b = Batch("B001", 100)
        b.fail_quality_control("Defect found")
        assert b.quality_status == "failed"
