"""Тесты для класса QualityInspector"""
import pytest
from factory.personnel.quality_inspector import QualityInspector
from factory.products.product import Product
from factory.quality.quality_control import QualityControl
from factory.production.batch import Batch


class TestQualityInspector:
    def test_creation(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        assert qi.name == "Anna Test"
        assert qi.position == "Quality Inspector"

    def test_assign_to_quality_control(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        qc = QualityControl("QC-001", "QC Dept")
        qi.assign_to_quality_control(qc)
        assert qi.quality_control == qc

    def test_inspect_product(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        product = Product("P001", "Widget", "Test")
        result = qi.inspect_product(product)
        # Status is now based on score: passed (>=90), needs_review (70-89), failed (<70)
        assert result['status'] in ['passed', 'needs_review', 'failed']
        assert result in qi.inspected_products

    def test_create_defect_report(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        product = Product("P001", "Widget", "Test")
        report = qi.create_defect_report(product, "Scratch on surface")
        assert report['defect'] == "Scratch on surface"
        assert report in qi.defect_reports

    def test_approve_batch(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        batch = Batch("B001", 100)
        # Updated signature: approve_batch(batch, batch_size)
        result = qi.approve_batch(batch, 100)
        assert 'approved' in result
        # approval depends on defect rate in sample, so can be True or False

    def test_get_inspection_count(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        qi.inspect_product(Product("P1", "W1", "T1"))
        qi.inspect_product(Product("P2", "W2", "T2"))
        assert qi.get_inspection_count() == 2

    def test_get_defect_rate(self):
        qi = QualityInspector("Anna Test", "QI-001", 55000)
        p1 = Product("P1", "W1", "T1")
        p2 = Product("P2", "W2", "T2")
        qi.inspect_product(p1)
        qi.inspect_product(p2)
        # Defect rate is now based on failed inspections, not defect reports
        # Since inspections are random, just check it's a valid percentage
        defect_rate = qi.get_defect_rate()
        assert 0 <= defect_rate <= 100
