"""Тесты для Shipment"""
import pytest
from factory.warehouse.shipment import Shipment
from datetime import datetime

class TestShipment:
    def test_creation(self):
        s = Shipment("SH001", datetime.now())
        assert s.shipment_id == "SH001"
        assert s.status == "pending"
    
    def test_prepare_and_ship(self):
        s = Shipment("SH001", datetime.now())
        s.prepare_shipment()
        assert s.status == "prepared"
        s.ship("TRACK123")
        assert s.status == "shipped"
        assert s.tracking_number == "TRACK123"
    
    def test_mark_delivered(self):
        s = Shipment("SH001", datetime.now())
        s.mark_delivered()
        assert s.status == "delivered"
