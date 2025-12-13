"""Тесты для FinanceDepartment"""
import pytest
from factory.finance.finance_department import FinanceDepartment
from datetime import datetime, timedelta
from unittest.mock import Mock


class TestFinanceDepartment:
    """Полный набор тестов для FinanceDepartment"""

    # ===== Тесты инициализации (5) =====
    def test_creation(self):
        """Тест создания финансового отдела"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert fd.department_id == "FIN001"
        assert fd.name == "Finance"
        assert fd.factory is None
        assert fd.accountants == []
        assert fd.payments == []
        assert fd.budgets == []
        assert fd.cash_balance == 100000.0

    def test_creation_initializes_collections(self):
        """Тест инициализации коллекций"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert fd.financial_reports == []
        assert fd.invoices == []
        assert fd.tax_records == []

    def test_creation_initializes_financial_values(self):
        """Тест инициализации финансовых значений"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert fd.total_revenue == 0.0
        assert fd.total_expenses == 0.0
        assert fd.accounts_receivable == 0.0
        assert fd.accounts_payable == 0.0

    def test_creation_sets_timestamps(self):
        """Тест установки временных меток"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert fd.created_at is not None
        assert fd.fiscal_year_start is not None

    def test_creation_with_different_names(self):
        """Тест создания с разными именами"""
        fd1 = FinanceDepartment("FIN001", "Main Finance")
        fd2 = FinanceDepartment("FIN002", "Regional Finance")
        assert fd1.name == "Main Finance"
        assert fd2.name == "Regional Finance"

    # ===== Тесты assign_to_factory (4) =====
    def test_assign_to_factory(self):
        """Тест назначения фабрике"""
        fd = FinanceDepartment("FIN001", "Finance")
        factory = Mock()
        result = fd.assign_to_factory(factory)
        assert fd.factory == factory
        factory.set_finance_department.assert_called_once_with(fd)
        assert result == factory

    def test_assign_to_factory_calls_set_method(self):
        """Тест вызова метода set_finance_department"""
        fd = FinanceDepartment("FIN001", "Finance")
        factory = Mock()
        factory.name = "Test Factory"
        fd.assign_to_factory(factory)
        assert factory.set_finance_department.called

    def test_assign_to_factory_replaces_existing(self):
        """Тест замены существующей фабрики"""
        fd = FinanceDepartment("FIN001", "Finance")
        factory1 = Mock()
        factory2 = Mock()
        fd.assign_to_factory(factory1)
        fd.assign_to_factory(factory2)
        assert fd.factory == factory2

    def test_assign_to_factory_returns_factory(self):
        """Тест возврата фабрики"""
        fd = FinanceDepartment("FIN001", "Finance")
        factory = Mock()
        result = fd.assign_to_factory(factory)
        assert result is factory

    # ===== Тесты add_accountant (6) =====
    def test_add_accountant(self):
        """Тест добавления бухгалтера"""
        fd = FinanceDepartment("FIN001", "Finance")
        accountant = Mock()
        accountant.name = "John"
        result = fd.add_accountant(accountant)
        assert accountant in fd.accountants
        accountant.assign_to_finance_department.assert_called_once_with(fd)
        assert result == accountant

    def test_add_accountant_calls_assign(self):
        """Тест вызова assign_to_finance_department"""
        fd = FinanceDepartment("FIN001", "Finance")
        accountant = Mock()
        accountant.name = "Jane"
        fd.add_accountant(accountant)
        assert accountant.assign_to_finance_department.called

    def test_add_accountant_duplicate(self):
        """Тест добавления дубликата бухгалтера"""
        fd = FinanceDepartment("FIN001", "Finance")
        accountant = Mock()
        accountant.name = "John"
        fd.add_accountant(accountant)
        result = fd.add_accountant(accountant)
        assert len(fd.accountants) == 1
        assert result == accountant

    def test_add_multiple_accountants(self):
        """Тест добавления нескольких бухгалтеров"""
        fd = FinanceDepartment("FIN001", "Finance")
        acc1 = Mock()
        acc1.name = "John"
        acc2 = Mock()
        acc2.name = "Jane"
        fd.add_accountant(acc1)
        fd.add_accountant(acc2)
        assert len(fd.accountants) == 2

    def test_add_accountant_increments_count(self):
        """Тест увеличения счетчика бухгалтеров"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert len(fd.accountants) == 0
        accountant = Mock()
        accountant.name = "Test"
        fd.add_accountant(accountant)
        assert len(fd.accountants) == 1

    def test_add_accountant_returns_accountant(self):
        """Тест возврата бухгалтера"""
        fd = FinanceDepartment("FIN001", "Finance")
        accountant = Mock()
        accountant.name = "Test"
        result = fd.add_accountant(accountant)
        assert result is accountant

    # ===== Тесты process_payment (12) =====
    def test_process_payment_incoming(self):
        """Тест обработки входящего платежа"""
        fd = FinanceDepartment("FIN001", "Finance")
        initial_balance = fd.cash_balance
        payment = fd.process_payment(5000.0, 'incoming', 'sales', 'Product sale')
        assert payment['amount'] == 5000.0
        assert payment['payment_type'] == 'incoming'
        assert fd.total_revenue == 5000.0
        assert fd.cash_balance == initial_balance + 5000.0

    def test_process_payment_outgoing(self):
        """Тест обработки исходящего платежа"""
        fd = FinanceDepartment("FIN001", "Finance")
        initial_balance = fd.cash_balance
        payment = fd.process_payment(3000.0, 'outgoing', 'salaries', 'Monthly payroll')
        assert payment['amount'] == 3000.0
        assert payment['payment_type'] == 'outgoing'
        assert fd.total_expenses == 3000.0
        assert fd.cash_balance == initial_balance - 3000.0

    def test_process_payment_invalid_amount(self):
        """Тест обработки платежа с неверной суммой"""
        fd = FinanceDepartment("FIN001", "Finance")
        with pytest.raises(ValueError, match="Payment amount must be positive"):
            fd.process_payment(0, 'incoming', 'test')
        with pytest.raises(ValueError):
            fd.process_payment(-100, 'incoming', 'test')

    def test_process_payment_invalid_type(self):
        """Тест обработки платежа с неверным типом"""
        fd = FinanceDepartment("FIN001", "Finance")
        with pytest.raises(ValueError, match="Payment type must be 'incoming' or 'outgoing'"):
            fd.process_payment(1000.0, 'invalid', 'test')

    def test_process_payment_creates_payment_record(self):
        """Тест создания записи о платеже"""
        fd = FinanceDepartment("FIN001", "Finance")
        payment = fd.process_payment(1000.0, 'incoming', 'sales')
        assert payment['payment_id'].startswith('PAY-')
        assert payment['status'] == 'completed'
        assert 'processed_at' in payment

    def test_process_payment_adds_to_list(self):
        """Тест добавления платежа в список"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert len(fd.payments) == 0
        fd.process_payment(1000.0, 'incoming', 'sales')
        assert len(fd.payments) == 1

    def test_process_payment_low_balance_warning(self):
        """Тест предупреждения о низком балансе"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.cash_balance = 15000.0
        fd.process_payment(10000.0, 'outgoing', 'expenses')
        assert fd.cash_balance == 5000.0  # Должно быть < 10000

    def test_process_payment_multiple_payments(self):
        """Тест обработки нескольких платежей"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.process_payment(1000.0, 'incoming', 'sales')
        fd.process_payment(500.0, 'outgoing', 'expenses')
        fd.process_payment(2000.0, 'incoming', 'sales')
        assert len(fd.payments) == 3
        assert fd.total_revenue == 3000.0
        assert fd.total_expenses == 500.0

    def test_process_payment_with_description(self):
        """Тест платежа с описанием"""
        fd = FinanceDepartment("FIN001", "Finance")
        payment = fd.process_payment(1000.0, 'incoming', 'sales', 'Test description')
        assert payment['description'] == 'Test description'

    def test_process_payment_without_description(self):
        """Тест платежа без описания"""
        fd = FinanceDepartment("FIN001", "Finance")
        payment = fd.process_payment(1000.0, 'incoming', 'sales')
        assert payment['description'] == ''

    def test_process_payment_sequential_ids(self):
        """Тест последовательных ID платежей"""
        fd = FinanceDepartment("FIN001", "Finance")
        p1 = fd.process_payment(100.0, 'incoming', 'test')
        p2 = fd.process_payment(200.0, 'incoming', 'test')
        assert p1['payment_id'] == 'PAY-0000001'
        assert p2['payment_id'] == 'PAY-0000002'

    def test_process_payment_updates_balance(self):
        """Тест обновления баланса"""
        fd = FinanceDepartment("FIN001", "Finance")
        initial = fd.cash_balance
        fd.process_payment(1000.0, 'incoming', 'test')
        fd.process_payment(500.0, 'outgoing', 'test')
        assert fd.cash_balance == initial + 1000.0 - 500.0

    # ===== Тесты create_invoice (8) =====
    def test_create_invoice(self):
        """Тест создания счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer A", 5000.0, due_date, "Product sale")
        assert invoice['customer'] == "Customer A"
        assert invoice['amount'] == 5000.0
        assert invoice['status'] == 'unpaid'
        assert fd.accounts_receivable == 5000.0

    def test_create_invoice_invalid_amount(self):
        """Тест создания счета с неверной суммой"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        with pytest.raises(ValueError, match="Invoice amount must be positive"):
            fd.create_invoice("Customer", 0, due_date)
        with pytest.raises(ValueError):
            fd.create_invoice("Customer", -100, due_date)

    def test_create_invoice_adds_to_list(self):
        """Тест добавления счета в список"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        assert len(fd.invoices) == 0
        fd.create_invoice("Customer", 1000.0, due_date)
        assert len(fd.invoices) == 1

    def test_create_invoice_updates_receivable(self):
        """Тест обновления дебиторской задолженности"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        initial = fd.accounts_receivable
        fd.create_invoice("Customer", 1000.0, due_date)
        assert fd.accounts_receivable == initial + 1000.0

    def test_create_invoice_sequential_ids(self):
        """Тест последовательных ID счетов"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        inv1 = fd.create_invoice("Customer1", 1000.0, due_date)
        inv2 = fd.create_invoice("Customer2", 2000.0, due_date)
        assert inv1['invoice_id'] == 'INV-0000001'
        assert inv2['invoice_id'] == 'INV-0000002'

    def test_create_invoice_with_description(self):
        """Тест создания счета с описанием"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date, "Test description")
        assert invoice['description'] == "Test description"

    def test_create_invoice_initializes_paid_amount(self):
        """Тест инициализации оплаченной суммы"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        assert invoice['paid_amount'] == 0.0

    def test_create_invoice_sets_dates(self):
        """Тест установки дат"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        assert 'issued_at' in invoice
        assert invoice['due_date'] == due_date

    # ===== Тесты receive_invoice_payment (12) =====
    def test_receive_invoice_payment_full(self):
        """Тест полной оплаты счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        result = fd.receive_invoice_payment(invoice['invoice_id'], 1000.0)
        assert result['status'] == 'paid'
        assert result['paid_amount'] == 1000.0

    def test_receive_invoice_payment_partial(self):
        """Тест частичной оплаты счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        result = fd.receive_invoice_payment(invoice['invoice_id'], 500.0)
        assert result['status'] == 'partial'
        assert result['paid_amount'] == 500.0

    def test_receive_invoice_payment_invalid_amount(self):
        """Тест оплаты с неверной суммой"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        with pytest.raises(ValueError, match="Payment amount must be positive"):
            fd.receive_invoice_payment(invoice['invoice_id'], 0)

    def test_receive_invoice_payment_not_found(self):
        """Тест оплаты несуществующего счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        with pytest.raises(ValueError, match="Invoice .* not found"):
            fd.receive_invoice_payment("INV-9999999", 100.0)

    def test_receive_invoice_payment_already_paid(self):
        """Тест оплаты уже оплаченного счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        fd.receive_invoice_payment(invoice['invoice_id'], 1000.0)
        result = fd.receive_invoice_payment(invoice['invoice_id'], 100.0)
        assert result['status'] == 'paid'

    def test_receive_invoice_payment_exceeds_amount(self):
        """Тест оплаты, превышающей сумму счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        result = fd.receive_invoice_payment(invoice['invoice_id'], 1500.0)
        assert result['paid_amount'] == 1000.0

    def test_receive_invoice_payment_updates_receivable(self):
        """Тест обновления дебиторской задолженности"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        fd.create_invoice("Customer", 1000.0, due_date)
        initial = fd.accounts_receivable
        fd.receive_invoice_payment('INV-0000001', 500.0)
        assert fd.accounts_receivable == initial - 500.0

    def test_receive_invoice_payment_processes_payment(self):
        """Тест обработки платежа"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        initial_payments = len(fd.payments)
        fd.receive_invoice_payment(invoice['invoice_id'], 500.0)
        assert len(fd.payments) == initial_payments + 1

    def test_receive_invoice_payment_sets_paid_at(self):
        """Тест установки даты оплаты"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        fd.receive_invoice_payment(invoice['invoice_id'], 1000.0)
        assert 'paid_at' in invoice

    def test_receive_invoice_payment_multiple_partial(self):
        """Тест нескольких частичных оплат"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        fd.receive_invoice_payment(invoice['invoice_id'], 300.0)
        fd.receive_invoice_payment(invoice['invoice_id'], 200.0)
        result = fd.receive_invoice_payment(invoice['invoice_id'], 500.0)
        assert result['status'] == 'paid'
        assert result['paid_amount'] == 1000.0

    def test_receive_invoice_payment_updates_revenue(self):
        """Тест обновления выручки"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        initial_revenue = fd.total_revenue
        fd.receive_invoice_payment(invoice['invoice_id'], 500.0)
        assert fd.total_revenue == initial_revenue + 500.0

    def test_receive_invoice_payment_returns_invoice(self):
        """Тест возврата счета"""
        fd = FinanceDepartment("FIN001", "Finance")
        due_date = datetime.now() + timedelta(days=30)
        invoice = fd.create_invoice("Customer", 1000.0, due_date)
        result = fd.receive_invoice_payment(invoice['invoice_id'], 500.0)
        assert result is invoice

    # ===== Тесты add_budget (8) =====
    def test_add_budget(self):
        """Тест добавления бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        budget = fd.add_budget("marketing", 50000.0, "annual")
        assert budget['category'] == "marketing"
        assert budget['allocated_amount'] == 50000.0
        assert budget['spent_amount'] == 0.0
        assert budget['status'] == 'active'

    def test_add_budget_invalid_amount(self):
        """Тест добавления бюджета с неверной суммой"""
        fd = FinanceDepartment("FIN001", "Finance")
        with pytest.raises(ValueError, match="Budget amount must be positive"):
            fd.add_budget("test", 0, "annual")
        with pytest.raises(ValueError):
            fd.add_budget("test", -1000, "annual")

    def test_add_budget_invalid_period(self):
        """Тест добавления бюджета с неверным периодом"""
        fd = FinanceDepartment("FIN001", "Finance")
        with pytest.raises(ValueError, match="Period must be"):
            fd.add_budget("test", 1000.0, "weekly")

    def test_add_budget_valid_periods(self):
        """Тест всех валидных периодов"""
        fd = FinanceDepartment("FIN001", "Finance")
        b1 = fd.add_budget("cat1", 1000.0, "monthly")
        b2 = fd.add_budget("cat2", 2000.0, "quarterly")
        b3 = fd.add_budget("cat3", 3000.0, "annual")
        assert b1['period'] == "monthly"
        assert b2['period'] == "quarterly"
        assert b3['period'] == "annual"

    def test_add_budget_adds_to_list(self):
        """Тест добавления бюджета в список"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert len(fd.budgets) == 0
        fd.add_budget("test", 1000.0, "annual")
        assert len(fd.budgets) == 1

    def test_add_budget_sequential_ids(self):
        """Тест последовательных ID бюджетов"""
        fd = FinanceDepartment("FIN001", "Finance")
        b1 = fd.add_budget("cat1", 1000.0, "annual")
        b2 = fd.add_budget("cat2", 2000.0, "annual")
        assert b1['budget_id'] == 'BUD-0001'
        assert b2['budget_id'] == 'BUD-0002'

    def test_add_budget_sets_created_at(self):
        """Тест установки времени создания"""
        fd = FinanceDepartment("FIN001", "Finance")
        budget = fd.add_budget("test", 1000.0, "annual")
        assert 'created_at' in budget

    def test_add_budget_multiple_categories(self):
        """Тест добавления бюджетов разных категорий"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("marketing", 10000.0, "annual")
        fd.add_budget("salaries", 50000.0, "annual")
        fd.add_budget("operations", 30000.0, "annual")
        assert len(fd.budgets) == 3

    # ===== Тесты check_budget_compliance (6) =====
    def test_check_budget_compliance_within_limit(self):
        """Тест соответствия бюджету в пределах лимита"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("marketing", 10000.0, "annual")
        assert fd.check_budget_compliance("marketing", 5000.0) is True

    def test_check_budget_compliance_exceeds_limit(self):
        """Тест превышения лимита бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        budget = fd.add_budget("marketing", 10000.0, "annual")
        budget['spent_amount'] = 8000.0
        assert fd.check_budget_compliance("marketing", 5000.0) is False

    def test_check_budget_compliance_no_budget(self):
        """Тест проверки без бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert fd.check_budget_compliance("nonexistent", 1000.0) is True

    def test_check_budget_compliance_exact_limit(self):
        """Тест точного лимита бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("marketing", 10000.0, "annual")
        assert fd.check_budget_compliance("marketing", 10000.0) is True

    def test_check_budget_compliance_inactive_budget(self):
        """Тест проверки с неактивным бюджетом"""
        fd = FinanceDepartment("FIN001", "Finance")
        budget = fd.add_budget("marketing", 10000.0, "annual")
        budget['status'] = 'inactive'
        assert fd.check_budget_compliance("marketing", 1000.0) is True

    def test_check_budget_compliance_partial_spent(self):
        """Тест проверки с частично потраченным бюджетом"""
        fd = FinanceDepartment("FIN001", "Finance")
        budget = fd.add_budget("marketing", 10000.0, "annual")
        budget['spent_amount'] = 5000.0
        assert fd.check_budget_compliance("marketing", 4000.0) is True
        assert fd.check_budget_compliance("marketing", 6000.0) is False

    # ===== Тесты create_financial_report (6) =====
    def test_create_financial_report(self):
        """Тест создания финансового отчета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.process_payment(10000.0, 'incoming', 'sales')
        fd.process_payment(6000.0, 'outgoing', 'expenses')
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        report = fd.create_financial_report(start, end)
        assert report['total_revenue'] == 10000.0
        assert report['total_expenses'] == 6000.0
        assert report['net_profit'] == 4000.0

    def test_create_financial_report_adds_to_list(self):
        """Тест добавления отчета в список"""
        fd = FinanceDepartment("FIN001", "Finance")
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        assert len(fd.financial_reports) == 0
        fd.create_financial_report(start, end)
        assert len(fd.financial_reports) == 1

    def test_create_financial_report_sequential_ids(self):
        """Тест последовательных ID отчетов"""
        fd = FinanceDepartment("FIN001", "Finance")
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        r1 = fd.create_financial_report(start, end)
        r2 = fd.create_financial_report(start, end)
        assert r1['report_id'] == 'REP-00001'
        assert r2['report_id'] == 'REP-00002'

    def test_create_financial_report_calculates_margin(self):
        """Тест расчета маржи прибыли"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.process_payment(10000.0, 'incoming', 'sales')
        fd.process_payment(5000.0, 'outgoing', 'expenses')
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        report = fd.create_financial_report(start, end)
        assert report['profit_margin'] == 50.0

    def test_create_financial_report_empty_period(self):
        """Тест отчета за пустой период"""
        fd = FinanceDepartment("FIN001", "Finance")
        start = datetime.now() + timedelta(days=10)
        end = datetime.now() + timedelta(days=20)
        report = fd.create_financial_report(start, end)
        assert report['total_revenue'] == 0.0
        assert report['total_expenses'] == 0.0
        assert report['net_profit'] == 0.0

    def test_create_financial_report_includes_balances(self):
        """Тест включения балансов в отчет"""
        fd = FinanceDepartment("FIN001", "Finance")
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        report = fd.create_financial_report(start, end)
        assert 'cash_balance' in report
        assert 'accounts_receivable' in report
        assert 'accounts_payable' in report

    # ===== Тесты calculate_tax_liability (6) =====
    def test_calculate_tax_liability(self):
        """Тест расчета налоговых обязательств"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        tax = fd.calculate_tax_liability(0.20)
        assert tax == 8000.0  # (100000 - 60000) * 0.20

    def test_calculate_tax_liability_no_profit(self):
        """Тест расчета налога без прибыли"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 50000.0
        fd.total_expenses = 50000.0
        tax = fd.calculate_tax_liability(0.20)
        assert tax == 0.0

    def test_calculate_tax_liability_negative_profit(self):
        """Тест расчета налога при убытке"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 50000.0
        fd.total_expenses = 80000.0
        tax = fd.calculate_tax_liability(0.20)
        assert tax == 0.0

    def test_calculate_tax_liability_invalid_rate(self):
        """Тест расчета налога с неверной ставкой"""
        fd = FinanceDepartment("FIN001", "Finance")
        with pytest.raises(ValueError, match="Tax rate must be between 0 and 1"):
            fd.calculate_tax_liability(-0.1)
        with pytest.raises(ValueError):
            fd.calculate_tax_liability(1.5)

    def test_calculate_tax_liability_creates_record(self):
        """Тест создания налоговой записи"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        assert len(fd.tax_records) == 0
        fd.calculate_tax_liability(0.20)
        assert len(fd.tax_records) == 1

    def test_calculate_tax_liability_different_rates(self):
        """Тест различных налоговых ставок"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        tax1 = fd.calculate_tax_liability(0.15)
        fd.total_revenue = 100000.0  # Reset
        fd.total_expenses = 60000.0
        tax2 = fd.calculate_tax_liability(0.25)
        assert tax1 == 6000.0
        assert tax2 == 10000.0

    # ===== Тесты get_net_profit (3) =====
    def test_get_net_profit(self):
        """Тест получения чистой прибыли"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        assert fd.get_net_profit() == 40000.0

    def test_get_net_profit_zero(self):
        """Тест нулевой прибыли"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 50000.0
        fd.total_expenses = 50000.0
        assert fd.get_net_profit() == 0.0

    def test_get_net_profit_negative(self):
        """Тест отрицательной прибыли (убыток)"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 50000.0
        fd.total_expenses = 80000.0
        assert fd.get_net_profit() == -30000.0

    # ===== Тесты get_profit_margin (4) =====
    def test_get_profit_margin(self):
        """Тест получения маржи прибыли"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        assert fd.get_profit_margin() == 40.0

    def test_get_profit_margin_zero_revenue(self):
        """Тест маржи при нулевой выручке"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 0.0
        fd.total_expenses = 5000.0
        assert fd.get_profit_margin() == 0.0

    def test_get_profit_margin_negative(self):
        """Тест отрицательной маржи"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 120000.0
        assert fd.get_profit_margin() == -20.0

    def test_get_profit_margin_high(self):
        """Тест высокой маржи"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 10000.0
        assert fd.get_profit_margin() == 90.0

    # ===== Тесты get_total_budget (4) =====
    def test_get_total_budget(self):
        """Тест получения общего бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("cat1", 10000.0, "annual")
        fd.add_budget("cat2", 20000.0, "annual")
        assert fd.get_total_budget() == 30000.0

    def test_get_total_budget_empty(self):
        """Тест общего бюджета при отсутствии бюджетов"""
        fd = FinanceDepartment("FIN001", "Finance")
        assert fd.get_total_budget() == 0.0

    def test_get_total_budget_inactive(self):
        """Тест исключения неактивных бюджетов"""
        fd = FinanceDepartment("FIN001", "Finance")
        b1 = fd.add_budget("cat1", 10000.0, "annual")
        b2 = fd.add_budget("cat2", 20000.0, "annual")
        b2['status'] = 'inactive'
        assert fd.get_total_budget() == 10000.0

    def test_get_total_budget_single(self):
        """Тест с одним бюджетом"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("test", 5000.0, "annual")
        assert fd.get_total_budget() == 5000.0

    # ===== Тесты get_budget_utilization (4) =====
    def test_get_budget_utilization(self):
        """Тест получения использования бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("test", 10000.0, "annual")
        fd.total_expenses = 5000.0
        assert fd.get_budget_utilization() == 50.0

    def test_get_budget_utilization_no_budget(self):
        """Тест использования при отсутствии бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_expenses = 5000.0
        assert fd.get_budget_utilization() == 0.0

    def test_get_budget_utilization_full(self):
        """Тест полного использования бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("test", 10000.0, "annual")
        fd.total_expenses = 10000.0
        assert fd.get_budget_utilization() == 100.0

    def test_get_budget_utilization_exceeded(self):
        """Тест превышения бюджета"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("test", 10000.0, "annual")
        fd.total_expenses = 15000.0
        assert fd.get_budget_utilization() == 150.0

    # ===== Тесты get_financial_health_score (6) =====
    def test_get_financial_health_score_excellent(self):
        """Тест отличного финансового здоровья"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0  # 40% margin
        fd.cash_balance = 150000.0
        fd.add_budget("test", 100000.0, "annual")
        score = fd.get_financial_health_score()
        assert score > 80

    def test_get_financial_health_score_poor(self):
        """Тест плохого финансового здоровья"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 99000.0  # 1% margin
        fd.cash_balance = 5000.0
        score = fd.get_financial_health_score()
        assert score < 50

    def test_get_financial_health_score_profitability(self):
        """Тест критерия прибыльности"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 75000.0  # 25% margin > 20
        score = fd.get_financial_health_score()
        assert score >= 40  # Should get 40 points for profitability

    def test_get_financial_health_score_liquidity(self):
        """Тест критерия ликвидности"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.cash_balance = 150000.0  # > 100000
        score = fd.get_financial_health_score()
        assert score >= 30  # Should get 30 points for liquidity

    def test_get_financial_health_score_receivables(self):
        """Тест критерия дебиторской задолженности"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.accounts_receivable = 5000.0  # < 10% of revenue
        score = fd.get_financial_health_score()
        assert score >= 15  # Should get 15 points for receivables

    def test_get_financial_health_score_budget_discipline(self):
        """Тест критерия бюджетной дисциплины"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.add_budget("test", 10000.0, "annual")
        fd.total_expenses = 8000.0  # 80% utilization
        score = fd.get_financial_health_score()
        assert score >= 15  # Should get 15 points for budget discipline

    # ===== Тесты get_financial_statistics (4) =====
    def test_get_financial_statistics(self):
        """Тест получения финансовой статистики"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        stats = fd.get_financial_statistics()
        assert stats['department_id'] == "FIN001"
        assert stats['total_revenue'] == 100000.0
        assert stats['total_expenses'] == 60000.0
        assert stats['net_profit'] == 40000.0

    def test_get_financial_statistics_includes_all_fields(self):
        """Тест наличия всех полей в статистике"""
        fd = FinanceDepartment("FIN001", "Finance")
        stats = fd.get_financial_statistics()
        required_fields = [
            'department_id', 'department_name', 'total_revenue', 'total_expenses',
            'net_profit', 'profit_margin', 'cash_balance', 'accounts_receivable',
            'accounts_payable', 'total_budget', 'budget_utilization',
            'financial_health_score', 'total_payments', 'total_invoices',
            'unpaid_invoices', 'active_budgets', 'total_reports', 'accountants_count'
        ]
        for field in required_fields:
            assert field in stats

    def test_get_financial_statistics_counts(self):
        """Тест счетчиков в статистике"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.process_payment(1000.0, 'incoming', 'test')
        due_date = datetime.now() + timedelta(days=30)
        fd.create_invoice("Customer", 500.0, due_date)
        fd.add_budget("test", 1000.0, "annual")
        stats = fd.get_financial_statistics()
        assert stats['total_payments'] == 1
        assert stats['total_invoices'] == 1
        assert stats['unpaid_invoices'] == 1
        assert stats['active_budgets'] == 1

    def test_get_financial_statistics_returns_dict(self):
        """Тест возврата словаря"""
        fd = FinanceDepartment("FIN001", "Finance")
        stats = fd.get_financial_statistics()
        assert isinstance(stats, dict)

    # ===== Тесты __repr__ (3) =====
    def test_repr(self):
        """Тест строкового представления"""
        fd = FinanceDepartment("FIN001", "Finance")
        fd.total_revenue = 100000.0
        fd.total_expenses = 60000.0
        result = repr(fd)
        assert "FinanceDepartment" in result
        assert "Finance" in result
        assert "40000" in result

    def test_repr_includes_health_score(self):
        """Тест включения оценки здоровья"""
        fd = FinanceDepartment("FIN001", "Finance")
        result = repr(fd)
        assert "/100" in result

    def test_repr_different_profits(self):
        """Тест представления с разными прибылями"""
        fd1 = FinanceDepartment("FIN001", "Finance1")
        fd1.total_revenue = 100000.0
        fd1.total_expenses = 40000.0
        fd2 = FinanceDepartment("FIN002", "Finance2")
        fd2.total_revenue = 50000.0
        fd2.total_expenses = 30000.0
        repr1 = repr(fd1)
        repr2 = repr(fd2)
        assert "60000" in repr1
        assert "20000" in repr2
