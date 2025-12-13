"""
Отчет о продажах - статистика продаж
"""
from datetime import datetime
from typing import List


class SalesReport:
    """Отчет о продажах"""

    def __init__(self, report_id: str, period_start: datetime, period_end: datetime):
        self.report_id = report_id
        self.period_start = period_start
        self.period_end = period_end
        self.orders = []
        self.sales_manager = None
        self.customers = []
        self.financial_report = None
        self.total_revenue = 0.0
        self.total_orders = 0
        self.generated_at = datetime.now()

    def add_order(self, order):
        """Добавить заказ"""
        self.orders.append(order)
        self.total_orders += 1
        if hasattr(order, 'total_amount'):
            self.total_revenue += order.total_amount

    def set_sales_manager(self, manager):
        """Установить менеджера по продажам"""
        self.sales_manager = manager
        manager.submit_sales_report(self)

    def add_customer(self, customer):
        """Добавить клиента"""
        self.customers.append(customer)

    def link_financial_report(self, financial_report):
        """Связать с финансовым отчетом"""
        self.financial_report = financial_report

    def calculate_average_order_value(self):
        """Рассчитать среднюю стоимость заказа"""
        if self.total_orders == 0:
            return 0
        return self.total_revenue / self.total_orders

    def get_top_customers(self, limit: int = 5):
        """Получить топ клиентов"""
        customer_sales = {}
        for order in self.orders:
            if hasattr(order, 'customer') and order.customer:
                customer_id = order.customer.customer_id
                if customer_id not in customer_sales:
                    customer_sales[customer_id] = {
                        'customer': order.customer,
                        'total': 0
                    }
                if hasattr(order, 'total_amount'):
                    customer_sales[customer_id]['total'] += order.total_amount

        sorted_customers = sorted(customer_sales.values(), key=lambda x: x['total'], reverse=True)
        return sorted_customers[:limit]

    def get_summary(self):
        """Получить сводку отчета"""
        return {
            'report_id': self.report_id,
            'period': f"{self.period_start} - {self.period_end}",
            'sales_manager': self.sales_manager.name if self.sales_manager else None,
            'total_revenue': self.total_revenue,
            'total_orders': self.total_orders,
            'average_order_value': self.calculate_average_order_value(),
            'customers_count': len(self.customers),
            'generated_at': self.generated_at
        }

    def __repr__(self):
        return f"SalesReport(id='{self.report_id}', revenue={self.total_revenue}, orders={self.total_orders})"
