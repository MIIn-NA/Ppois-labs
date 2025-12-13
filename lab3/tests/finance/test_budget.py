"""Тесты для Budget"""
import pytest
from factory.finance.budget import Budget
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock


class TestBudget:
    """Расширенный набор тестов для класса Budget - полное покрытие"""

    # ===== Тесты инициализации (10) =====
    def test_creation_with_valid_data(self):
        """Тест создания бюджета с корректными данными"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        assert b.budget_id == "BUD001"
        assert b.period_start == start
        assert b.period_end == end
        assert b.allocated_amount == 100000.0
        assert b.status == "active"

    def test_creation_initializes_empty_expenses(self):
        """Тест инициализации пустого списка расходов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        assert b.expenses == []

    def test_creation_initializes_zero_spent(self):
        """Тест инициализации нулевых расходов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        assert b.spent_amount == 0.0

    def test_creation_sets_default_departments(self):
        """Тест инициализации отделов как None"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        assert b.department is None
        assert b.finance_department is None

    def test_creation_with_different_periods(self):
        """Тест создания с разными периодами"""
        start = datetime(2024, 6, 1)
        end = datetime(2024, 8, 31)
        b = Budget("BUD002", start, end, 50000.0)
        assert b.period_start == start
        assert b.period_end == end

    def test_creation_with_large_allocated_amount(self):
        """Тест создания с большой выделенной суммой"""
        b = Budget("BUD003", datetime.now(), datetime.now(), 10000000.0)
        assert b.allocated_amount == 10000000.0

    def test_creation_with_zero_allocated_amount(self):
        """Тест создания с нулевой выделенной суммой"""
        b = Budget("BUD004", datetime.now(), datetime.now(), 0.0)
        assert b.allocated_amount == 0.0
        assert b.status == "active"

    def test_creation_with_fractional_amount(self):
        """Тест создания с дробной выделенной суммой"""
        b = Budget("BUD005", datetime.now(), datetime.now(), 12345.67)
        assert b.allocated_amount == 12345.67

    def test_creation_with_string_budget_id(self):
        """Тест создания с различными форматами ID"""
        b1 = Budget("BUDGET-2024-001", datetime.now(), datetime.now(), 100000.0)
        b2 = Budget("B_001", datetime.now(), datetime.now(), 50000.0)
        assert b1.budget_id == "BUDGET-2024-001"
        assert b2.budget_id == "B_001"

    def test_creation_with_same_start_and_end_dates(self):
        """Тест создания с одинаковыми датами начала и конца"""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        b = Budget("BUD006", dt, dt, 100000.0)
        assert b.period_start == dt
        assert b.period_end == dt

    # ===== Тесты установки отдела (5) =====
    def test_set_department(self):
        """Тест установки отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        mock_dept = Mock()
        b.set_department(mock_dept)
        assert b.department == mock_dept
        mock_dept.set_budget.assert_called_once_with(b)

    def test_set_department_calls_set_budget(self):
        """Тест вызова set_budget при установке отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        mock_dept = Mock()
        b.set_department(mock_dept)
        mock_dept.set_budget.assert_called_once()

    def test_set_department_replaces_existing(self):
        """Тест замены существующего отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        old_dept = Mock()
        new_dept = Mock()
        b.set_department(old_dept)
        assert b.department == old_dept
        b.set_department(new_dept)
        assert b.department == new_dept

    def test_set_department_multiple_times(self):
        """Тест многократной установки отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        dept1 = Mock()
        dept2 = Mock()
        dept3 = Mock()
        b.set_department(dept1)
        b.set_department(dept2)
        b.set_department(dept3)
        assert b.department == dept3
        assert dept3.set_budget.called

    def test_set_department_with_different_mock_types(self):
        """Тест установки отдела с разными типами mock объектов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        magic_dept = MagicMock()
        b.set_department(magic_dept)
        assert b.department == magic_dept

    # ===== Тесты установки финансового отдела (5) =====
    def test_set_finance_department(self):
        """Тест установки финансового отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        mock_finance_dept = Mock()
        b.set_finance_department(mock_finance_dept)
        assert b.finance_department == mock_finance_dept
        mock_finance_dept.add_budget.assert_called_once_with(b)

    def test_set_finance_department_calls_add_budget(self):
        """Тест вызова add_budget при установке финансового отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        mock_finance_dept = Mock()
        b.set_finance_department(mock_finance_dept)
        mock_finance_dept.add_budget.assert_called_once()

    def test_set_finance_department_replaces_existing(self):
        """Тест замены существующего финансового отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        old_finance_dept = Mock()
        new_finance_dept = Mock()
        b.set_finance_department(old_finance_dept)
        assert b.finance_department == old_finance_dept
        b.set_finance_department(new_finance_dept)
        assert b.finance_department == new_finance_dept

    def test_set_finance_department_multiple_times(self):
        """Тест многократной установки финансового отдела"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        fd1 = Mock()
        fd2 = Mock()
        b.set_finance_department(fd1)
        b.set_finance_department(fd2)
        assert b.finance_department == fd2

    def test_set_both_departments(self):
        """Тест установки обоих отделов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        dept = Mock()
        finance_dept = Mock()
        b.set_department(dept)
        b.set_finance_department(finance_dept)
        assert b.department == dept
        assert b.finance_department == finance_dept

    # ===== Тесты добавления расходов (15) =====
    def test_add_expense_with_amount(self):
        """Тест добавления расхода с атрибутом amount"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        mock_expense = Mock()
        mock_expense.amount = 5000.0
        b.add_expense(mock_expense)
        assert mock_expense in b.expenses
        assert b.spent_amount == 5000.0

    def test_add_multiple_expenses(self):
        """Тест добавления нескольких расходов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        for i in range(5):
            expense = Mock()
            expense.amount = 10000.0
            b.add_expense(expense)
        assert len(b.expenses) == 5
        assert b.spent_amount == 50000.0

    def test_add_expense_without_amount_attribute(self):
        """Тест добавления расхода без атрибута amount"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        mock_expense = Mock(spec=[])
        b.add_expense(mock_expense)
        assert mock_expense in b.expenses
        assert b.spent_amount == 0.0

    def test_add_expense_changes_status_to_depleted(self):
        """Тест изменения статуса на depleted при исчерпании бюджета"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        expense1 = Mock()
        expense1.amount = 5000.0
        expense2 = Mock()
        expense2.amount = 5000.0
        b.add_expense(expense1)
        assert b.status == "active"
        b.add_expense(expense2)
        assert b.status == "depleted"

    def test_add_expense_exceeding_budget(self):
        """Тест добавления расхода, превышающего бюджет"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        expense = Mock()
        expense.amount = 15000.0
        b.add_expense(expense)
        assert b.spent_amount == 15000.0
        assert b.status == "depleted"

    def test_add_expense_with_zero_amount(self):
        """Тест добавления расхода с нулевой суммой"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        expense = Mock()
        expense.amount = 0.0
        b.add_expense(expense)
        assert b.spent_amount == 0.0
        assert b.status == "active"

    def test_add_expense_partial_depletion(self):
        """Тест добавления расходов до частичного использования"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        expense = Mock()
        expense.amount = 75000.0
        b.add_expense(expense)
        assert b.spent_amount == 75000.0
        assert b.status == "active"

    def test_add_expense_exact_depletion(self):
        """Тест добавления расхода, точно исчерпывающего бюджет"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        expense = Mock()
        expense.amount = 100000.0
        b.add_expense(expense)
        assert b.spent_amount == 100000.0
        assert b.status == "depleted"

    def test_add_large_expense(self):
        """Тест добавления большого расхода"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 1000000.0)
        expense = Mock()
        expense.amount = 999999.99
        b.add_expense(expense)
        assert b.spent_amount == 999999.99

    def test_add_fractional_expense(self):
        """Тест добавления расхода с дробной суммой"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        expense = Mock()
        expense.amount = 3333.33
        b.add_expense(expense)
        assert abs(b.spent_amount - 3333.33) < 0.01

    def test_add_many_small_expenses(self):
        """Тест добавления множества маленьких расходов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        for i in range(100):
            expense = Mock()
            expense.amount = 50.0
            b.add_expense(expense)
        assert b.spent_amount == 5000.0
        assert len(b.expenses) == 100

    def test_add_expense_to_depleted_budget(self):
        """Тест добавления расхода к уже исчерпанному бюджету"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        exp1 = Mock()
        exp1.amount = 10000.0
        b.add_expense(exp1)
        assert b.status == "depleted"
        exp2 = Mock()
        exp2.amount = 1000.0
        b.add_expense(exp2)
        assert b.spent_amount == 11000.0
        assert b.status == "depleted"

    def test_add_expense_incremental_accumulation(self):
        """Тест постепенного накопления расходов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100.0)
        amounts = [10.5, 20.3, 15.7, 30.1, 24.4]
        for amount in amounts:
            expense = Mock()
            expense.amount = amount
            b.add_expense(expense)
        assert abs(b.spent_amount - 101.0) < 0.1
        assert b.status == "depleted"

    def test_add_expense_with_negative_amount(self):
        """Тест добавления расхода с отрицательной суммой (нестандартный случай)"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        expense = Mock()
        expense.amount = -500.0
        b.add_expense(expense)
        assert b.spent_amount == -500.0
        assert b.status == "active"

    def test_add_expense_mixed_with_and_without_amounts(self):
        """Тест добавления расходов с amount и без него"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        exp1 = Mock()
        exp1.amount = 1000.0
        exp2 = Mock(spec=[])  # без amount
        exp3 = Mock()
        exp3.amount = 2000.0
        b.add_expense(exp1)
        b.add_expense(exp2)
        b.add_expense(exp3)
        assert len(b.expenses) == 3
        assert b.spent_amount == 3000.0

    # ===== Тесты получения оставшейся суммы (8) =====
    def test_get_remaining_amount_with_partial_spending(self):
        """Тест получения оставшейся суммы при частичном использовании"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 60000.0
        assert b.get_remaining_amount() == 40000.0

    def test_get_remaining_amount_no_spending(self):
        """Тест получения оставшейся суммы при нулевых расходах"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        assert b.get_remaining_amount() == 100000.0

    def test_get_remaining_amount_full_spending(self):
        """Тест получения оставшейся суммы при полном использовании"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 100000.0
        assert b.get_remaining_amount() == 0.0

    def test_get_remaining_amount_overspending(self):
        """Тест получения оставшейся суммы при превышении бюджета"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 150000.0
        assert b.get_remaining_amount() == 0.0

    def test_get_remaining_amount_with_zero_budget(self):
        """Тест получения оставшейся суммы при нулевом бюджете"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 0.0)
        assert b.get_remaining_amount() == 0.0

    def test_get_remaining_amount_with_fractional_values(self):
        """Тест получения оставшейся суммы с дробными значениями"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 12345.67)
        b.spent_amount = 5432.10
        assert abs(b.get_remaining_amount() - 6913.57) < 0.01

    def test_get_remaining_amount_after_expenses(self):
        """Тест получения оставшейся суммы после добавления расходов"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 50000.0)
        exp = Mock()
        exp.amount = 12345.67
        b.add_expense(exp)
        assert abs(b.get_remaining_amount() - 37654.33) < 0.01

    def test_get_remaining_amount_very_small_remaining(self):
        """Тест получения очень маленькой оставшейся суммы"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = 9999.99
        assert abs(b.get_remaining_amount() - 0.01) < 0.001

    # ===== Тесты получения процента использования (10) =====
    def test_get_utilization_percentage_no_spending(self):
        """Тест процента использования при нулевых расходах"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        assert b.get_utilization_percentage() == 0.0

    def test_get_utilization_percentage_50_percent(self):
        """Тест процента использования 50%"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 50000.0
        assert b.get_utilization_percentage() == 50.0

    def test_get_utilization_percentage_100_percent(self):
        """Тест процента использования 100%"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 100000.0
        assert b.get_utilization_percentage() == 100.0

    def test_get_utilization_percentage_over_100_percent(self):
        """Тест процента использования более 100%"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 150000.0
        assert b.get_utilization_percentage() == 150.0

    def test_get_utilization_percentage_with_zero_budget(self):
        """Тест процента использования при нулевом бюджете"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 0.0)
        assert b.get_utilization_percentage() == 0.0

    def test_get_utilization_percentage_fractional_values(self):
        """Тест процента использования с дробными значениями"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 200000.0)
        b.spent_amount = 75000.0
        assert b.get_utilization_percentage() == 37.5

    def test_get_utilization_percentage_small_amounts(self):
        """Тест процента использования с малыми суммами"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 1000.0)
        b.spent_amount = 333.33
        assert abs(b.get_utilization_percentage() - 33.333) < 0.01

    def test_get_utilization_percentage_large_amounts(self):
        """Тест процента использования с большими суммами"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000000.0)
        b.spent_amount = 2500000.0
        assert b.get_utilization_percentage() == 25.0

    def test_get_utilization_percentage_very_low(self):
        """Тест очень низкого процента использования"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 1000000.0)
        b.spent_amount = 100.0
        assert abs(b.get_utilization_percentage() - 0.01) < 0.001

    def test_get_utilization_percentage_after_add_expense(self):
        """Тест процента использования после добавления расхода"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        exp = Mock()
        exp.amount = 2500.0
        b.add_expense(exp)
        assert b.get_utilization_percentage() == 25.0

    # ===== Тесты проверки исчерпания (8) =====
    def test_is_depleted_false(self):
        """Тест проверки на исчерпание бюджета - false"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 50000.0
        assert b.is_depleted() is False

    def test_is_depleted_true(self):
        """Тест проверки на исчерпание бюджета - true"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 100000.0
        assert b.is_depleted() is True

    def test_is_depleted_over_limit(self):
        """Тест проверки на исчерпание при превышении бюджета"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 150000.0
        assert b.is_depleted() is True

    def test_is_depleted_no_spending(self):
        """Тест проверки на исчерпание при нулевых расходах"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        assert b.is_depleted() is False

    def test_is_depleted_with_zero_budget(self):
        """Тест проверки на исчерпание при нулевом бюджете"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 0.0)
        assert b.is_depleted() is True

    def test_is_depleted_almost_depleted(self):
        """Тест проверки на исчерпание при почти полном использовании"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 99999.99
        assert b.is_depleted() is False

    def test_is_depleted_exactly_at_boundary(self):
        """Тест проверки на исчерпание ровно на границе"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 50000.0)
        b.spent_amount = 50000.0
        assert b.is_depleted() is True

    def test_is_depleted_after_negative_expense(self):
        """Тест проверки на исчерпание после отрицательного расхода"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = -1000.0
        assert b.is_depleted() is False

    # ===== Тесты проверки истечения (8) =====
    def test_check_expiration_not_expired(self):
        """Тест проверки истечения - бюджет еще активен"""
        start = datetime(2024, 1, 1)
        end = datetime(2025, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        result = b.check_expiration()
        assert result is False
        assert b.status == "active"

    def test_check_expiration_expired(self):
        """Тест проверки истечения - бюджет истекший"""
        start = datetime(2020, 1, 1)
        end = datetime(2020, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        result = b.check_expiration()
        assert result is True
        assert b.status == "expired"

    def test_check_expiration_already_expired(self):
        """Тест проверки истечения уже истекшего бюджета"""
        start = datetime(2020, 1, 1)
        end = datetime(2020, 6, 30)
        b = Budget("BUD001", start, end, 100000.0)
        b.status = "expired"
        result = b.check_expiration()
        assert result is False
        assert b.status == "expired"

    def test_check_expiration_depleted_budget(self):
        """Тест проверки истечения исчерпанного бюджета"""
        start = datetime(2020, 1, 1)
        end = datetime(2020, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        b.status = "depleted"
        result = b.check_expiration()
        assert result is False

    def test_check_expiration_boundary(self):
        """Тест проверки истечения на границе периода"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 6, 30, 23, 59, 59)
        b = Budget("BUD001", start, end, 100000.0)
        result = b.check_expiration()
        assert isinstance(result, bool)

    def test_check_expiration_far_future(self):
        """Тест проверки истечения для бюджета в далеком будущем"""
        start = datetime(2030, 1, 1)
        end = datetime(2030, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        result = b.check_expiration()
        assert result is False
        assert b.status == "active"

    def test_check_expiration_past_budget(self):
        """Тест проверки истечения для старого бюджета"""
        start = datetime(2015, 1, 1)
        end = datetime(2015, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        result = b.check_expiration()
        assert result is True
        assert b.status == "expired"

    def test_check_expiration_multiple_calls(self):
        """Тест многократной проверки истечения"""
        start = datetime(2020, 1, 1)
        end = datetime(2020, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        result1 = b.check_expiration()
        result2 = b.check_expiration()
        result3 = b.check_expiration()
        assert result1 is True
        assert result2 is False
        assert result3 is False
        assert b.status == "expired"

    # ===== Тесты увеличения выделения (12) =====
    def test_increase_allocation(self):
        """Тест увеличения выделенной суммы"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.increase_allocation(50000.0)
        assert b.allocated_amount == 150000.0

    def test_increase_allocation_multiple_times(self):
        """Тест множественного увеличения выделенной суммы"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.increase_allocation(30000.0)
        b.increase_allocation(20000.0)
        b.increase_allocation(10000.0)
        assert b.allocated_amount == 160000.0

    def test_increase_allocation_zero_amount(self):
        """Тест увеличения на нулевую сумму"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.increase_allocation(0.0)
        assert b.allocated_amount == 100000.0

    def test_increase_allocation_restores_active_status(self):
        """Тест восстановления активного статуса при увеличении"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = 10000.0
        b.status = "depleted"
        b.increase_allocation(5000.0)
        assert b.allocated_amount == 15000.0
        assert b.status == "active"

    def test_increase_allocation_not_enough_to_restore(self):
        """Тест увеличения, недостаточного для восстановления"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = 12000.0
        b.status = "depleted"
        b.increase_allocation(1000.0)
        assert b.allocated_amount == 11000.0
        assert b.status == "depleted"

    def test_increase_allocation_exact_recovery(self):
        """Тест увеличения на точное восстановление"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = 10000.0
        b.status = "depleted"
        b.increase_allocation(10000.0)
        assert b.allocated_amount == 20000.0
        assert b.status == "active"

    def test_increase_allocation_on_active_status(self):
        """Тест увеличения при активном статусе"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 50000.0
        b.status = "active"
        b.increase_allocation(30000.0)
        assert b.status == "active"

    def test_increase_allocation_large_amount(self):
        """Тест увеличения на большую сумму"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.increase_allocation(900000.0)
        assert b.allocated_amount == 1000000.0

    def test_increase_allocation_fractional_amount(self):
        """Тест увеличения на дробную сумму"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.increase_allocation(1234.56)
        assert abs(b.allocated_amount - 11234.56) < 0.01

    def test_increase_allocation_on_expired_budget(self):
        """Тест увеличения истекшего бюджета (не меняет статус)"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.status = "expired"
        b.spent_amount = 5000.0
        b.increase_allocation(5000.0)
        assert b.allocated_amount == 15000.0
        assert b.status == "expired"  # статус не меняется с expired

    def test_increase_allocation_barely_above_spent(self):
        """Тест увеличения чуть выше потраченного"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = 10000.0
        b.status = "depleted"
        b.increase_allocation(0.01)
        assert b.allocated_amount == 10000.01
        assert b.status == "active"

    def test_increase_allocation_with_negative_spent(self):
        """Тест увеличения при отрицательных затратах"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 10000.0)
        b.spent_amount = -1000.0
        b.increase_allocation(5000.0)
        assert b.allocated_amount == 15000.0
        assert b.status == "active"

    # ===== Тесты строкового представления (5) =====
    def test_repr(self):
        """Тест строкового представления"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 50000.0
        result = repr(b)
        assert "BUD001" in result
        assert "100000" in result
        assert "50000" in result
        assert "active" in result
        assert "Budget" in result

    def test_repr_depleted(self):
        """Тест представления исчерпанного бюджета"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.spent_amount = 100000.0
        b.status = "depleted"
        result = repr(b)
        assert "depleted" in result

    def test_repr_expired(self):
        """Тест представления истекшего бюджета"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 100000.0)
        b.status = "expired"
        result = repr(b)
        assert "expired" in result

    def test_repr_with_zero_amounts(self):
        """Тест представления с нулевыми суммами"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 0.0)
        result = repr(b)
        assert "BUD001" in result
        assert "0" in result

    def test_repr_with_large_amounts(self):
        """Тест представления с большими суммами"""
        b = Budget("BUD001", datetime.now(), datetime.now(), 9999999.99)
        b.spent_amount = 8888888.88
        result = repr(b)
        assert "BUD001" in result
        assert "9999999.99" in result
        assert "8888888.88" in result

    # ===== Интеграционные тесты (7) =====
    def test_integration_full_budget_lifecycle(self):
        """Интеграционный тест полного жизненного цикла бюджета"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        b = Budget("BUD001", start, end, 100000.0)
        mock_dept = Mock()
        mock_finance_dept = Mock()
        b.set_department(mock_dept)
        b.set_finance_department(mock_finance_dept)
        for i in range(3):
            expense = Mock()
            expense.amount = 25000.0
            b.add_expense(expense)
        assert len(b.expenses) == 3
        assert b.spent_amount == 75000.0
        assert b.get_remaining_amount() == 25000.0
        assert b.get_utilization_percentage() == 75.0
        assert b.is_depleted() is False
        assert b.status == "active"

    def test_integration_budget_with_depletion_and_increase(self):
        """Интеграционный тест исчерпания и увеличения бюджета"""
        b = Budget("BUD002", datetime.now(), datetime.now(), 50000.0)
        expense1 = Mock()
        expense1.amount = 30000.0
        expense2 = Mock()
        expense2.amount = 20000.0
        b.add_expense(expense1)
        b.add_expense(expense2)
        assert b.is_depleted() is True
        assert b.status == "depleted"
        b.increase_allocation(30000.0)
        assert b.allocated_amount == 80000.0
        assert b.status == "active"
        assert b.get_remaining_amount() == 30000.0

    def test_integration_budget_with_multiple_operations(self):
        """Интеграционный тест с множеством операций"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        b = Budget("BUD003", start, end, 100000.0)
        expenses_amounts = [10000.0, 15000.0, 20000.0, 12000.0, 8000.0]
        for amount in expenses_amounts:
            expense = Mock()
            expense.amount = amount
            b.add_expense(expense)
        assert b.spent_amount == 65000.0
        assert b.get_remaining_amount() == 35000.0
        assert b.get_utilization_percentage() == 65.0
        assert not b.is_depleted()
        b.increase_allocation(50000.0)
        assert b.allocated_amount == 150000.0
        assert b.get_remaining_amount() == 85000.0

    def test_integration_zero_budget_operations(self):
        """Интеграционный тест операций с нулевым бюджетом"""
        b = Budget("BUD004", datetime.now(), datetime.now(), 0.0)
        assert b.get_remaining_amount() == 0.0
        assert b.get_utilization_percentage() == 0.0
        assert b.is_depleted() is True
        expense = Mock()
        expense.amount = 100.0
        b.add_expense(expense)
        assert b.spent_amount == 100.0
        assert b.is_depleted() is True
        b.increase_allocation(150.0)
        assert b.allocated_amount == 150.0
        assert b.status == "active"

    def test_integration_high_precision_amounts(self):
        """Интеграционный тест с высокой точностью сумм"""
        b = Budget("BUD005", datetime.now(), datetime.now(), 123456.789)
        expense1 = Mock()
        expense1.amount = 45678.123
        expense2 = Mock()
        expense2.amount = 32109.456
        b.add_expense(expense1)
        b.add_expense(expense2)
        assert abs(b.spent_amount - 77787.579) < 0.01
        assert abs(b.get_remaining_amount() - 45669.21) < 0.01
        assert abs(b.get_utilization_percentage() - 63.0093) < 0.1

    def test_integration_complex_scenario(self):
        """Интеграционный тест сложного сценария"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        b = Budget("COMPLEX001", start, end, 250000.0)

        # Установка отделов
        dept = Mock()
        finance_dept = Mock()
        b.set_department(dept)
        b.set_finance_department(finance_dept)

        # Добавление расходов
        for i in range(10):
            exp = Mock()
            exp.amount = 20000.0
            b.add_expense(exp)

        assert b.spent_amount == 200000.0
        assert b.get_remaining_amount() == 50000.0
        assert b.get_utilization_percentage() == 80.0
        assert b.is_depleted() is False

        # Добавляем еще расходов до исчерпания
        exp = Mock()
        exp.amount = 60000.0
        b.add_expense(exp)

        assert b.is_depleted() is True
        assert b.status == "depleted"

        # Увеличиваем бюджет
        b.increase_allocation(100000.0)
        assert b.status == "active"
        assert b.get_remaining_amount() == 90000.0

    def test_integration_budget_expiration_with_spending(self):
        """Интеграционный тест истечения бюджета с расходами"""
        start = datetime(2020, 1, 1)
        end = datetime(2020, 12, 31)
        b = Budget("EXPIRED001", start, end, 100000.0)

        # Добавляем расходы
        exp = Mock()
        exp.amount = 50000.0
        b.add_expense(exp)

        assert b.spent_amount == 50000.0
        assert b.status == "active"

        # Проверяем истечение
        result = b.check_expiration()
        assert result is True
        assert b.status == "expired"

        # Проверяем, что расходы сохранились
        assert b.spent_amount == 50000.0
        assert b.get_remaining_amount() == 50000.0
