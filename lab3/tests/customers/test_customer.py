"""Тесты для Customer"""
import pytest
from factory.customers.customer import Customer

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock


class TestCustomer:
    """Расширенный набор тестов для класса Customer"""

    # ===== Тесты инициализации =====
    def test_creation_with_valid_data(self):
        """Тест создания клиента с корректными данными"""
        c = Customer("CUS001", "John Smith", "john@example.com")
        assert c.customer_id == "CUS001"
        assert c.name == "John Smith"
        assert c.contact_info == "john@example.com"
        assert c.is_active is True

    def test_creation_initializes_empty_collections(self):
        """Тест инициализации пустых коллекций"""
        c = Customer("CUS001", "John Smith", "john@example.com")
        assert c.orders == []
        assert c.contracts == []
        assert c.payments == []

    def test_creation_sets_default_values(self):
        """Тест установки значений по умолчанию"""
        c = Customer("CUS001", "John Smith", "john@example.com")
        assert c.customer_type == "regular"
        assert c.credit_limit == 0.0
        assert c.current_balance == 0.0
        assert c.price_list is None

    def test_creation_sets_timestamp(self):
        """Тест установки временной метки создания"""
        before_creation = datetime.now()
        c = Customer("CUS001", "John Smith", "john@example.com")
        after_creation = datetime.now()

        assert before_creation <= c.created_at <= after_creation

    def test_creation_with_special_characters_in_name(self):

        c = Customer("CUS001", "Иван Петров", "ivan@example.com")
        assert c.name == "Иван Петров"

    def test_creation_with_special_characters_in_contact(self):
        """Тест создания со спецсимволами в контакте"""
        c = Customer("CUS001", "John Smith", "+7 (999) 123-45-67")
        assert c.contact_info == "+7 (999) 123-45-67"

    # ===== Тесты работы с заказами =====
