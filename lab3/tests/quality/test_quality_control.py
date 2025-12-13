"""Тесты для QualityControl"""
import pytest
from factory.quality.quality_control import QualityControl
from factory.production.batch import Batch
from factory.personnel.quality_inspector import QualityInspector

class TestQualityControl:
    def test_creation(self):
        qc = QualityControl("QC001", "Quality Control")
        assert qc.qc_id == "QC001"
        assert qc.name == "Quality Control"
    
    def test_inspect_batch(self):
        qc = QualityControl("QC001", "QC")
        b = Batch("B001", 100)
        qi = QualityInspector("Anna", "QI001", 55000)
        result = qc.inspect_batch(b, qi)
        assert result['passed'] is True
    
    def test_get_pass_rate(self):
        qc = QualityControl("QC001", "QC")
        qc.total_inspections = 100
        qc.total_passed = 95
        assert qc.get_pass_rate() == 95.0
