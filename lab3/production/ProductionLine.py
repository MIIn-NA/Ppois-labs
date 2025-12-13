"""
Производственная линия - линия сборки/производства
"""
from datetime import datetime, timedelta
from typing import List, Dict


class ProductionLine:
    """Производственная линия"""

    def __init__(self, line_id: str, name: str):
        self.line_id = line_id
        self.name = name
        self.factory = None
        self.machines = []
        self.workers = []
        self.products = []
        self.production_orders = []
        self.completed_orders = []
        self.is_operational = False
        self.production_volume = 0
        self.max_capacity = 1000  # единиц в день
        self.min_workers_required = 3
        self.min_machines_required = 2
        self.created_at = datetime.now()
        self.total_downtime_hours = 0.0
        self.quality_issues = []
        self.last_maintenance_check = datetime.now()

    def assign_to_factory(self, factory):
        """
        Назначить на фабрику с регистрацией

        Автоматически добавляет линию в список фабрики
        """
        if self.factory is not None:
            print(f"Warning: Production line {self.name} is being transferred from {self.factory.name}")

        self.factory = factory
        factory.add_production_line(self)

        print(f"Production line '{self.name}' assigned to factory '{factory.name}'")

        return factory

    def add_machine(self, machine):
        """
        Добавить станок с проверкой совместимости

        Валидирует работоспособность и тип станка
        """
        if machine in self.machines:
            print(f"Warning: Machine {machine.name} is already on this production line")
            return machine

        # Проверка работоспособности станка
        if hasattr(machine, 'is_operational') and not machine.is_operational:
            print(f"Warning: Adding non-operational machine {machine.name} to production line")

        self.machines.append(machine)
        machine.assign_to_production_line(self)

        print(f"Machine '{machine.name}' added to production line '{self.name}'")
        print(f"Total machines: {len(self.machines)}")

        return machine

    def remove_machine(self, machine):
        """Удалить станок из линии"""
        if machine in self.machines:
            self.machines.remove(machine)
            print(f"Machine {machine.name} removed from production line '{self.name}'")
            return True
        return False

    def add_worker(self, worker):
        """
        Добавить рабочего с проверкой квалификации

        Валидирует активность и соответствие требованиям
        """
        if worker in self.workers:
            print(f"Warning: Worker {worker.name} is already on this production line")
            return worker

        # Проверка активности рабочего
        if hasattr(worker, 'is_active') and not worker.is_active:
            raise RuntimeError(f"Cannot assign inactive worker {worker.name} to production line")

        # Проверка минимальной квалификации (если установлена)
        if hasattr(self, 'min_skill_level') and hasattr(worker, 'skill_level'):
            if worker.skill_level < self.min_skill_level:
                raise ValueError(
                    f"Worker {worker.name} skill level {worker.skill_level} is below minimum {self.min_skill_level}"
                )

        self.workers.append(worker)
        worker.assign_to_production_line(self)

        print(f"Worker '{worker.name}' added to production line '{self.name}'")
        print(f"Total workers: {len(self.workers)}")

        return worker

    def remove_worker(self, worker):
        """Удалить рабочего из линии"""
        if worker in self.workers:
            self.workers.remove(worker)
            print(f"Worker {worker.name} removed from production line '{self.name}'")
            return True
        return False

    def add_product(self, product):
        """
        Добавить продукт в ассортимент линии

        Регистрирует тип продукта для производства
        """
        if product not in self.products:
            self.products.append(product)
            print(f"Product '{product}' added to production line '{self.name}'")

        return product

    def create_production_order(self, product, quantity: int, priority: str = "normal"):
        """
        Создать производственный заказ с планированием

        Валидирует емкость и создает график выполнения
        """
        if quantity <= 0:
            raise ValueError("Production order quantity must be positive")

        if priority not in ["low", "normal", "high", "urgent"]:
            raise ValueError("Priority must be 'low', 'normal', 'high', or 'urgent'")

        # Расчет времени выполнения
        production_rate = self._calculate_production_rate()
        estimated_days = (quantity / production_rate) if production_rate > 0 else 0

        order = {
            'order_id': f"PO-{len(self.production_orders) + 1:06d}",
            'product': product.name if hasattr(product, 'name') else str(product),
            'quantity': quantity,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now(),
            'estimated_completion': datetime.now() + timedelta(days=estimated_days),
            'estimated_days': round(estimated_days, 2),
            'completed_quantity': 0
        }

        self.production_orders.append(order)

        print(f"Production order created: {order['order_id']}")
        print(f"Product: {order['product']} | Quantity: {quantity} | Est. days: {estimated_days:.1f}")

        return order

    def _calculate_production_rate(self) -> float:
        """Рассчитать скорость производства на основе ресурсов"""
        if not self.machines or not self.workers:
            return 0.0

        # Базовая производительность от станков
        operational_machines = len([m for m in self.machines if hasattr(m, 'is_operational') and m.is_operational])
        machine_capacity = operational_machines * 50  # 50 единиц на станок в день

        # Эффективность рабочих
        worker_efficiency = len(self.workers) * 30  # 30 единиц на рабочего в день

        # Берем минимум (узкое место)
        return min(machine_capacity, worker_efficiency, self.max_capacity)

    def start_production(self):
        """
        Запустить производство с полными проверками

        Валидирует готовность всех компонентов
        """
        if self.is_operational:
            print(f"Warning: Production line '{self.name}' is already operational")
            return False

        # Проверка минимальных требований
        if len(self.machines) < self.min_machines_required:
            raise RuntimeError(
                f"Cannot start production: minimum {self.min_machines_required} machines required, have {len(self.machines)}"
            )

        if len(self.workers) < self.min_workers_required:
            raise RuntimeError(
                f"Cannot start production: minimum {self.min_workers_required} workers required, have {len(self.workers)}"
            )

        # Проверка работоспособности станков
        operational_machines = [m for m in self.machines if hasattr(m, 'is_operational') and m.is_operational]
        if len(operational_machines) == 0:
            raise RuntimeError("Cannot start production: no operational machines available")

        # Проверка активных рабочих
        active_workers = [w for w in self.workers if hasattr(w, 'is_active') and w.is_active]
        if len(active_workers) == 0:
            raise RuntimeError("Cannot start production: no active workers available")

        self.is_operational = True

        result = {
            'line': self.name,
            'line_id': self.line_id,
            'started_at': datetime.now(),
            'machines': len(self.machines),
            'operational_machines': len(operational_machines),
            'workers': len(active_workers),
            'production_rate': self._calculate_production_rate()
        }

        print(f"Production line '{self.name}' started successfully")
        print(f"Operational machines: {len(operational_machines)}/{len(self.machines)}")
        print(f"Active workers: {len(active_workers)}")
        print(f"Production rate: {result['production_rate']:.0f} units/day")

        return result

    def stop_production(self, reason: str = "Planned shutdown"):
        """
        Остановить производство с записью причины

        Логирует остановку для анализа простоев
        """
        if not self.is_operational:
            print(f"Warning: Production line '{self.name}' is not operational")
            return False

        self.is_operational = False

        result = {
            'line': self.name,
            'line_id': self.line_id,
            'stopped_at': datetime.now(),
            'reason': reason
        }

        print(f"Production line '{self.name}' stopped: {reason}")

        return result

    def record_downtime(self, hours: float, reason: str):
        """
        Записать простой линии

        Отслеживает время и причины простоев
        """
        if hours <= 0:
            raise ValueError("Downtime hours must be positive")

        self.total_downtime_hours += hours

        downtime_record = {
            'hours': hours,
            'reason': reason,
            'timestamp': datetime.now()
        }

        print(f"Downtime recorded for '{self.name}': {hours}h - {reason}")
        print(f"Total downtime: {self.total_downtime_hours:.2f}h")

        return downtime_record

    def get_production_volume(self):
        """Получить объем производства"""
        return self.production_volume

    def increase_production_volume(self, amount: int):
        """
        Увеличить объем производства с валидацией

        Проверяет корректность и обновляет статистику
        """
        if amount <= 0:
            raise ValueError("Production volume increase must be positive")

        if not self.is_operational:
            print(f"Warning: Increasing production volume on non-operational line '{self.name}'")

        self.production_volume += amount

        print(f"Production volume increased by {amount}. Total: {self.production_volume}")

        return self.production_volume

    def get_efficiency(self):
        """
        Получить эффективность линии с детальным расчетом

        Учитывает работоспособность станков, наличие рабочих и простои
        """
        if not self.machines:
            return 0.0

        # Эффективность станков
        operational_machines = len([m for m in self.machines if hasattr(m, 'is_operational') and m.is_operational])
        machine_efficiency = (operational_machines / len(self.machines)) * 100

        # Эффективность укомплектованности рабочими
        worker_ratio = min(1.0, len(self.workers) / max(1, self.min_workers_required))
        worker_efficiency = worker_ratio * 100

        # Штраф за простои
        uptime_hours = (datetime.now() - self.created_at).total_seconds() / 3600
        downtime_penalty = (self.total_downtime_hours / uptime_hours * 100) if uptime_hours > 0 else 0

        # Итоговая эффективность
        total_efficiency = (machine_efficiency * 0.6 + worker_efficiency * 0.4) - downtime_penalty

        return round(max(0, total_efficiency), 2)

    def get_status_report(self) -> Dict:
        """
        Получить полный статус линии

        Возвращает детальную информацию о состоянии
        """
        operational_machines = len([m for m in self.machines if hasattr(m, 'is_operational') and m.is_operational])
        active_workers = len([w for w in self.workers if hasattr(w, 'is_active') and w.is_active])

        report = {
            'line_id': self.line_id,
            'line_name': self.name,
            'is_operational': self.is_operational,
            'machines_total': len(self.machines),
            'machines_operational': operational_machines,
            'workers_total': len(self.workers),
            'workers_active': active_workers,
            'production_volume': self.production_volume,
            'efficiency': self.get_efficiency(),
            'production_rate': self._calculate_production_rate(),
            'pending_orders': len([o for o in self.production_orders if o['status'] == 'pending']),
            'completed_orders': len(self.completed_orders),
            'total_downtime_hours': round(self.total_downtime_hours, 2),
            'quality_issues_count': len(self.quality_issues)
        }

        return report

    def __repr__(self):
        return f"ProductionLine(name='{self.name}', machines={len(self.machines)}, operational={self.is_operational})"
