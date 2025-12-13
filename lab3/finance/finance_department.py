"""
Финансовый отдел - управление финансами
"""
from datetime import datetime, timedelta
from typing import List, Dict


class FinanceDepartment:
    """Финансовый отдел"""

    def __init__(self, department_id: str, name: str):
        self.department_id = department_id
        self.name = name
        self.factory = None
        self.accountants = []
        self.payments = []
        self.budgets = []
        self.financial_reports = []
        self.invoices = []
        self.tax_records = []
        self.total_revenue = 0.0
        self.total_expenses = 0.0
        self.accounts_receivable = 0.0  # Дебиторская задолженность
        self.accounts_payable = 0.0  # Кредиторская задолженность
        self.cash_balance = 100000.0  # Начальный баланс
        self.created_at = datetime.now()
        self.fiscal_year_start = datetime.now()

    def assign_to_factory(self, factory):
        """
        Назначить фабрике с регистрацией

        Устанавливает финансовый отдел как главный
        """
        self.factory = factory
        factory.set_finance_department(self)

        print(f"Finance Department '{self.name}' assigned to factory '{factory.name}'")

        return factory

    def add_accountant(self, accountant):
        """
        Добавить бухгалтера с валидацией

        Регистрирует бухгалтера в отделе
        """
        if accountant in self.accountants:
            print(f"Warning: Accountant {accountant.name} is already in this department")
            return accountant

        self.accountants.append(accountant)
        accountant.assign_to_finance_department(self)

        print(f"Accountant '{accountant.name}' added to Finance Department")
        print(f"Total accountants: {len(self.accountants)}")

        return accountant

    def process_payment(self, amount: float, payment_type: str, category: str, description: str = ""):
        """
        Обработать платеж с детальной записью

        Учитывает тип и категорию платежа
        """
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        if payment_type not in ['incoming', 'outgoing']:
            raise ValueError("Payment type must be 'incoming' or 'outgoing'")

        payment = {
            'payment_id': f"PAY-{len(self.payments) + 1:07d}",
            'amount': amount,
            'payment_type': payment_type,
            'category': category,
            'description': description,
            'processed_at': datetime.now(),
            'status': 'completed'
        }

        self.payments.append(payment)

        # Обновление финансов
        if payment_type == 'incoming':
            self.total_revenue += amount
            self.cash_balance += amount
            print(f"Revenue received: {amount:.2f} ({category})")
        else:  # outgoing
            self.total_expenses += amount
            self.cash_balance -= amount
            print(f"Expense paid: {amount:.2f} ({category})")

        print(f"Cash balance: {self.cash_balance:.2f}")

        # Предупреждение о низком балансе
        if self.cash_balance < 10000:
            print(f"WARNING: Low cash balance ({self.cash_balance:.2f})")

        return payment

    def create_invoice(self, customer: str, amount: float, due_date: datetime, description: str = ""):
        """
        Создать счет для клиента

        Регистрирует дебиторскую задолженность
        """
        if amount <= 0:
            raise ValueError("Invoice amount must be positive")

        invoice = {
            'invoice_id': f"INV-{len(self.invoices) + 1:07d}",
            'customer': customer,
            'amount': amount,
            'description': description,
            'issued_at': datetime.now(),
            'due_date': due_date,
            'status': 'unpaid',
            'paid_amount': 0.0
        }

        self.invoices.append(invoice)
        self.accounts_receivable += amount

        days_until_due = (due_date - datetime.now()).days

        print(f"Invoice created: {invoice['invoice_id']}")
        print(f"Customer: {customer} | Amount: {amount:.2f} | Due in {days_until_due} days")

        return invoice

    def receive_invoice_payment(self, invoice_id: str, amount: float):
        """
        Получить оплату по счету

        Уменьшает дебиторскую задолженность
        """
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        # Поиск счета
        invoice = None
        for inv in self.invoices:
            if inv['invoice_id'] == invoice_id:
                invoice = inv
                break

        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        if invoice['status'] == 'paid':
            print(f"Warning: Invoice {invoice_id} is already paid")
            return invoice

        # Проверка суммы
        remaining = invoice['amount'] - invoice['paid_amount']
        if amount > remaining:
            print(f"Warning: Payment amount ({amount:.2f}) exceeds remaining balance ({remaining:.2f})")
            amount = remaining

        # Обновление счета
        invoice['paid_amount'] += amount
        self.accounts_receivable -= amount

        # Обработка платежа
        self.process_payment(amount, 'incoming', 'invoice_payment', f"Payment for {invoice_id}")

        # Проверка полной оплаты
        if invoice['paid_amount'] >= invoice['amount']:
            invoice['status'] = 'paid'
            invoice['paid_at'] = datetime.now()
            print(f"Invoice {invoice_id} FULLY PAID")
        else:
            invoice['status'] = 'partial'
            print(f"Partial payment received: {amount:.2f}")
            print(f"Remaining: {invoice['amount'] - invoice['paid_amount']:.2f}")

        return invoice

    def add_budget(self, category: str, allocated_amount: float, period: str = "annual"):
        """
        Добавить бюджет с планированием

        Устанавливает лимиты расходов
        """
        if allocated_amount <= 0:
            raise ValueError("Budget amount must be positive")

        if period not in ['monthly', 'quarterly', 'annual']:
            raise ValueError("Period must be 'monthly', 'quarterly', or 'annual'")

        budget = {
            'budget_id': f"BUD-{len(self.budgets) + 1:04d}",
            'category': category,
            'allocated_amount': allocated_amount,
            'spent_amount': 0.0,
            'period': period,
            'created_at': datetime.now(),
            'status': 'active'
        }

        self.budgets.append(budget)

        print(f"Budget created: {category}")
        print(f"Allocated: {allocated_amount:.2f} ({period})")

        return budget

    def check_budget_compliance(self, category: str, amount: float) -> bool:
        """
        Проверить соответствие бюджету

        Валидирует возможность расхода
        """
        # Поиск активного бюджета
        budget = None
        for b in self.budgets:
            if b['category'] == category and b['status'] == 'active':
                budget = b
                break

        if not budget:
            print(f"Warning: No active budget found for category '{category}'")
            return True  # Разрешить если нет бюджета

        # Проверка лимита
        remaining = budget['allocated_amount'] - budget['spent_amount']

        if amount > remaining:
            print(f"BUDGET EXCEEDED for {category}")
            print(f"Requested: {amount:.2f} | Available: {remaining:.2f}")
            return False

        return True

    def create_financial_report(self, period_start: datetime, period_end: datetime):
        """
        Создать финансовый отчет за период

        Генерирует детальную финансовую отчетность
        """
        # Фильтрация платежей за период
        period_payments = [
            p for p in self.payments
            if period_start <= p['processed_at'] <= period_end
        ]

        period_revenue = sum(
            p['amount'] for p in period_payments
            if p['payment_type'] == 'incoming'
        )

        period_expenses = sum(
            p['amount'] for p in period_payments
            if p['payment_type'] == 'outgoing'
        )

        period_profit = period_revenue - period_expenses

        report = {
            'report_id': f"REP-{len(self.financial_reports) + 1:05d}",
            'period_start': period_start,
            'period_end': period_end,
            'total_revenue': round(period_revenue, 2),
            'total_expenses': round(period_expenses, 2),
            'net_profit': round(period_profit, 2),
            'profit_margin': round((period_profit / period_revenue * 100) if period_revenue > 0 else 0, 2),
            'cash_balance': round(self.cash_balance, 2),
            'accounts_receivable': round(self.accounts_receivable, 2),
            'accounts_payable': round(self.accounts_payable, 2),
            'total_payments': len(period_payments),
            'generated_at': datetime.now()
        }

        self.financial_reports.append(report)

        print(f"Financial Report generated: {report['report_id']}")
        print(f"Period: {period_start.date()} to {period_end.date()}")
        print(f"Revenue: {period_revenue:.2f} | Expenses: {period_expenses:.2f}")
        print(f"Net Profit: {period_profit:.2f} | Margin: {report['profit_margin']:.1f}%")

        return report

    def calculate_tax_liability(self, tax_rate: float = 0.20) -> float:
        """
        Рассчитать налоговые обязательства

        Определяет сумму налога на прибыль
        """
        if not 0 <= tax_rate <= 1:
            raise ValueError("Tax rate must be between 0 and 1")

        net_profit = self.get_net_profit()

        if net_profit <= 0:
            print("No tax liability - net profit is zero or negative")
            return 0.0

        tax_amount = net_profit * tax_rate

        tax_record = {
            'period': datetime.now().strftime('%Y-%m'),
            'taxable_income': round(net_profit, 2),
            'tax_rate': tax_rate,
            'tax_amount': round(tax_amount, 2),
            'calculated_at': datetime.now()
        }

        self.tax_records.append(tax_record)

        print(f"Tax liability calculated: {tax_amount:.2f}")
        print(f"Taxable income: {net_profit:.2f} | Rate: {tax_rate*100:.1f}%")

        return round(tax_amount, 2)

    def get_net_profit(self):
        """Получить чистую прибыль"""
        return round(self.total_revenue - self.total_expenses, 2)

    def get_profit_margin(self):
        """
        Получить маржу прибыли в процентах

        Показатель рентабельности
        """
        if self.total_revenue == 0:
            return 0.0

        margin = (self.get_net_profit() / self.total_revenue) * 100
        return round(margin, 2)

    def get_total_budget(self):
        """Получить общий выделенный бюджет"""
        total = sum(
            b['allocated_amount'] for b in self.budgets
            if b['status'] == 'active'
        )
        return round(total, 2)

    def get_budget_utilization(self):
        """
        Получить использование бюджета в процентах

        Показывает насколько израсходован бюджет
        """
        total_budget = self.get_total_budget()

        if total_budget == 0:
            return 0.0

        utilization = (self.total_expenses / total_budget) * 100
        return round(utilization, 2)

    def get_financial_health_score(self) -> float:
        """
        Оценить финансовое здоровье компании

        Возвращает оценку от 0 до 100
        """
        score = 0.0

        # Критерий 1: Прибыльность (40 баллов)
        profit_margin = self.get_profit_margin()
        if profit_margin > 20:
            score += 40
        elif profit_margin > 10:
            score += 30
        elif profit_margin > 0:
            score += 20

        # Критерий 2: Ликвидность (30 баллов)
        if self.cash_balance > 100000:
            score += 30
        elif self.cash_balance > 50000:
            score += 20
        elif self.cash_balance > 10000:
            score += 10

        # Критерий 3: Дебиторская задолженность (15 баллов)
        if self.accounts_receivable < self.total_revenue * 0.1:
            score += 15
        elif self.accounts_receivable < self.total_revenue * 0.2:
            score += 10

        # Критерий 4: Бюджетная дисциплина (15 баллов)
        budget_util = self.get_budget_utilization()
        if 70 <= budget_util <= 90:
            score += 15
        elif 50 <= budget_util <= 100:
            score += 10

        return round(score, 2)

    def get_financial_statistics(self) -> Dict:
        """
        Получить полную финансовую статистику

        Возвращает детальный финансовый обзор
        """
        stats = {
            'department_id': self.department_id,
            'department_name': self.name,
            'total_revenue': round(self.total_revenue, 2),
            'total_expenses': round(self.total_expenses, 2),
            'net_profit': self.get_net_profit(),
            'profit_margin': self.get_profit_margin(),
            'cash_balance': round(self.cash_balance, 2),
            'accounts_receivable': round(self.accounts_receivable, 2),
            'accounts_payable': round(self.accounts_payable, 2),
            'total_budget': self.get_total_budget(),
            'budget_utilization': self.get_budget_utilization(),
            'financial_health_score': self.get_financial_health_score(),
            'total_payments': len(self.payments),
            'total_invoices': len(self.invoices),
            'unpaid_invoices': len([i for i in self.invoices if i['status'] == 'unpaid']),
            'active_budgets': len([b for b in self.budgets if b['status'] == 'active']),
            'total_reports': len(self.financial_reports),
            'accountants_count': len(self.accountants)
        }

        return stats

    def __repr__(self):
        return f"FinanceDepartment(name='{self.name}', profit={self.get_net_profit():.2f}, health={self.get_financial_health_score():.1f}/100)"
