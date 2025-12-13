"""Тесты для TechnicalDocumentation"""
import pytest
from factory.quality.technical_documentation import TechnicalDocumentation

class TestTechnicalDocumentation:
    def test_creation(self):
        doc = TechnicalDocumentation("DOC001", "User Manual", "manual")
        assert doc.doc_id == "DOC001"
        assert doc.title == "User Manual"
        assert doc.status == "draft"
    
    def test_update_version(self):
        doc = TechnicalDocumentation("DOC001", "Manual", "manual")
        doc.update_version("2.0")
        assert doc.version == "2.0"
    
    def test_workflow(self):
        doc = TechnicalDocumentation("DOC001", "Manual", "manual")
        doc.submit_for_review()
        assert doc.status == "review"
        doc.approve()
        assert doc.status == "approved"
        assert doc.is_approved() is True
