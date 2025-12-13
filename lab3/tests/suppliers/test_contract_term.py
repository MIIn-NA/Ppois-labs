"""Тесты для ContractTerm"""
import pytest
from factory.suppliers.contract_term import ContractTerm

class TestContractTerm:
    def test_creation(self):
        t = ContractTerm("TERM001", "pricing", "Fixed price")
        assert t.term_id == "TERM001"
        assert t.term_type == "pricing"
        assert t.is_mandatory is True
    
    def test_update_description(self):
        t = ContractTerm("TERM001", "pricing", "Fixed price")
        t.update_description("Variable pricing")
        assert t.description == "Variable pricing"
