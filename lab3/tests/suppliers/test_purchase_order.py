"""Тесты для PurchaseOrder"""
import pytest
from factory.suppliers.purchase_order import PurchaseOrder
from datetime import datetime

class TestPurchaseOrder:
    def test_creation(self):
        po = PurchaseOrder("PO001", datetime.now())
        assert po.order_id == "PO001"
        assert po.status == "pending"
    
    def test_add_raw_material(self):
        po = PurchaseOrder("PO001", datetime.now())
        from factory.products.raw_material import RawMaterial
        m = RawMaterial("M1", "Steel", 10.0)
        po.add_raw_material(m, 100, 10.0)
        assert po.total_amount == 1000.0
    
    def test_workflow(self):
        po = PurchaseOrder("PO001", datetime.now())
        po.approve()
        assert po.status == "approved"
        po.mark_shipped()
        assert po.status == "shipped"
        po.mark_delivered()
        assert po.status == "delivered"
