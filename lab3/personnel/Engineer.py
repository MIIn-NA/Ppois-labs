"""
Инженер - обслуживает оборудование
"""
from datetime import datetime, timedelta
from typing import List, Dict
import random


class Engineer:
    """Инженер"""

    def __init__(self, name: str, employee_id: str, salary: float, specialization: str):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.specialization = specialization
        self.department = None
        self.machines = []
        self.maintenance_requests = []
        self.completed_maintenances = []
        self.technical_docs = []
        self.hire_date = datetime.now()
        self.is_active = True
        self.position = "Engineer"
        self.certifications = []
        self.experience_level = 1  # 1-5
        self.emergency_response_count = 0
        self.total_repair_hours = 0.0
        self.successful_repairs = 0
        self.failed_diagnoses = 0

    def assign_machine(self, machine):
        """
        Назначить станок для обслуживания с проверкой компетенции

        Проверяет совместимость специализации и наличие сертификации
        """
        if not self.is_active:
            raise RuntimeError(f"Cannot assign machines to inactive engineer {self.name}")

        # Проверка совместимости специализации
        if hasattr(machine, 'machine_type'):
            if self.specialization != "Universal" and machine.machine_type != self.specialization:
                print(f"Warning: Engineer {self.name} ({self.specialization}) assigned to {machine.machine_type} machine")

        # Проверка лимита станков
        max_machines = 5 + (self.experience_level * 2)
        if len(self.machines) >= max_machines:
            raise ValueError(
                f"Engineer {self.name} has reached maximum machine capacity ({max_machines})"
            )

        if machine not in self.machines:
            self.machines.append(machine)
            print(f"Engineer {self.name} assigned to machine '{machine.name}'")

        return machine

    def create_maintenance_request(self, machine, priority: str, description: str):
        """
        Создать заявку на обслуживание с приоритизацией

        Оценивает срочность и назначает временные рамки
        """
        if priority not in ["low", "medium", "high", "critical"]:
            raise ValueError("Priority must be 'low', 'medium', 'high', or 'critical'")

        # Определение временных рамок
        deadline_hours = {
            "low": 72,
            "medium": 24,
            "high": 8,
            "critical": 2
        }

        request = {
            'request_id': f"MNT-{len(self.maintenance_requests) + 1:04d}",
            'machine': machine,
            'engineer': self.name,
            'priority': priority,
            'description': description,
            'created_at': datetime.now(),
            'deadline': datetime.now() + timedelta(hours=deadline_hours[priority]),
            'status': 'pending'
        }

        self.maintenance_requests.append(request)

        if priority == "critical":
            print(f"CRITICAL MAINTENANCE REQUEST: {description}")
            print(f"Machine: {machine.name if hasattr(machine, 'name') else machine}")
            print(f"Deadline: {request['deadline']}")
        else:
            print(f"Maintenance request created: {request['request_id']} (Priority: {priority})")

        return request

    def perform_maintenance(self, machine, maintenance_type: str = "routine"):
        """
        Выполнить обслуживание с расчетом времени и эффективности

        Симулирует процесс обслуживания с учетом опыта инженера
        """
        if not self.is_active:
            raise RuntimeError("Inactive engineer cannot perform maintenance")

        if machine not in self.machines:
            print(f"Warning: {self.name} is not assigned to this machine. Assigning now...")
            self.assign_machine(machine)

        # Расчет времени обслуживания на основе опыта
        base_hours = {
            "routine": 2.0,
            "repair": 6.0,
            "overhaul": 12.0,
            "emergency": 4.0
        }

        time_multiplier = max(0.5, 1.5 - (self.experience_level * 0.2))
        maintenance_hours = base_hours.get(maintenance_type, 2.0) * time_multiplier

        # Симуляция успешности ремонта
        success_probability = min(0.95, 0.6 + (self.experience_level * 0.07))
        is_successful = random.random() < success_probability

        maintenance_record = {
            'maintenance_id': f"MNT-{len(self.completed_maintenances) + 1:05d}",
            'engineer': self.name,
            'machine': machine.name if hasattr(machine, 'name') else str(machine),
            'type': maintenance_type,
            'timestamp': datetime.now(),
            'duration_hours': round(maintenance_hours, 2),
            'status': 'completed' if is_successful else 'requires_followup',
            'success': is_successful
        }

        # Обновление статистики
        self.completed_maintenances.append(maintenance_record)
        self.total_repair_hours += maintenance_hours

        if is_successful:
            self.successful_repairs += 1
            # Восстановление работоспособности машины
            if hasattr(machine, 'is_operational'):
                machine.is_operational = True

        if maintenance_type == "emergency":
            self.emergency_response_count += 1

        print(f"[{self.name}] Completed {maintenance_type} maintenance on {maintenance_record['machine']}")
        print(f"Duration: {maintenance_hours:.2f}h | Status: {maintenance_record['status']}")

        return maintenance_record

    def add_technical_documentation(self, doc_name: str, machine, content: str):
        """
        Добавить техническую документацию с категоризацией

        Систематизирует документацию для быстрого доступа
        """
        doc = {
            'doc_id': f"DOC-{len(self.technical_docs) + 1:04d}",
            'name': doc_name,
            'machine': machine.name if hasattr(machine, 'name') else str(machine),
            'content': content,
            'author': self.name,
            'created_at': datetime.now(),
            'category': self._categorize_document(doc_name)
        }

        self.technical_docs.append(doc)

        print(f"Technical documentation added: {doc_name} (Category: {doc['category']})")

        return doc

    def _categorize_document(self, doc_name: str) -> str:
        """Внутренний метод для категоризации документации"""
        doc_lower = doc_name.lower()

        if "manual" in doc_lower or "guide" in doc_lower:
            return "manual"
        elif "repair" in doc_lower or "maintenance" in doc_lower:
            return "maintenance"
        elif "safety" in doc_lower:
            return "safety"
        elif "diagnostic" in doc_lower or "troubleshoot" in doc_lower:
            return "diagnostic"
        else:
            return "general"

    def diagnose_problem(self, machine, symptoms: str):
        """
        Диагностировать проблему с детальным анализом

        Использует опыт и знания для определения причины неисправности
        """
        if not self.is_active:
            raise RuntimeError("Inactive engineer cannot perform diagnostics")

        # Симуляция диагностики на основе опыта
        diagnostic_accuracy = min(0.95, 0.5 + (self.experience_level * 0.09))
        is_accurate = random.random() < diagnostic_accuracy

        # Определение сложности проблемы
        complexity = self._assess_complexity(symptoms)

        # Возможные диагнозы
        diagnoses = [
            "mechanical_wear",
            "electrical_failure",
            "software_malfunction",
            "lubrication_needed",
            "calibration_required",
            "component_replacement_needed"
        ]

        diagnosis_result = {
            'diagnostic_id': f"DIAG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'machine': machine.name if hasattr(machine, 'name') else str(machine),
            'symptoms': symptoms,
            'engineer': self.name,
            'diagnosis': random.choice(diagnoses) if is_accurate else "requires_inspection",
            'complexity': complexity,
            'confidence': diagnostic_accuracy * 100,
            'recommended_action': self._recommend_action(complexity),
            'estimated_repair_hours': complexity * 2,
            'timestamp': datetime.now()
        }

        if not is_accurate:
            self.failed_diagnoses += 1

        print(f"Diagnostic completed: {diagnosis_result['diagnosis']}")
        print(f"Confidence: {diagnosis_result['confidence']:.1f}% | Complexity: {complexity}/5")

        return diagnosis_result

    def _assess_complexity(self, symptoms: str) -> int:
        """Оценить сложность проблемы по симптомам"""
        complexity_keywords = {
            5: ["complete failure", "catastrophic", "system-wide"],
            4: ["severe", "critical", "multiple", "intermittent"],
            3: ["moderate", "recurring", "abnormal"],
            2: ["minor", "slight", "occasional"],
            1: ["routine", "normal", "preventive"]
        }

        symptoms_lower = symptoms.lower()

        for level, keywords in complexity_keywords.items():
            if any(keyword in symptoms_lower for keyword in keywords):
                return level

        return 3  # default moderate complexity

    def _recommend_action(self, complexity: int) -> str:
        """Рекомендовать действия на основе сложности"""
        actions = {
            1: "routine_maintenance",
            2: "schedule_repair",
            3: "priority_repair",
            4: "immediate_attention",
            5: "emergency_shutdown_and_overhaul"
        }
        return actions.get(complexity, "schedule_repair")

    def add_certification(self, cert_name: str, issuing_body: str):
        """
        Добавить сертификацию инженеру

        Повышает квалификацию и расширяет компетенции
        """
        cert = {
            'name': cert_name,
            'issuing_body': issuing_body,
            'date_obtained': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=730)  # 2 года
        }

        self.certifications.append(cert)

        print(f"Certification added for {self.name}: {cert_name}")
        print(f"Valid until: {cert['valid_until'].date()}")

        return cert

    def increase_experience_level(self):
        """
        Повысить уровень опыта

        Требует минимального количества завершенных работ
        """
        if self.experience_level >= 5:
            print(f"Engineer {self.name} is already at maximum experience level")
            return False

        required_repairs = self.experience_level * 20
        if self.successful_repairs < required_repairs:
            raise ValueError(
                f"Insufficient experience: {self.successful_repairs}/{required_repairs} successful repairs"
            )

        self.experience_level += 1
        self.salary *= 1.12  # 12% повышение зарплаты

        print(f"Engineer {self.name} promoted to experience level {self.experience_level}")
        print(f"New salary: {self.salary:.2f}")

        return True

    def get_performance_metrics(self) -> Dict:
        """
        Получить метрики производительности инженера

        Возвращает детальную статистику работы
        """
        total_maintenances = len(self.completed_maintenances)
        success_rate = (self.successful_repairs / total_maintenances * 100) if total_maintenances > 0 else 0

        metrics = {
            'name': self.name,
            'specialization': self.specialization,
            'experience_level': self.experience_level,
            'assigned_machines': len(self.machines),
            'total_maintenances': total_maintenances,
            'successful_repairs': self.successful_repairs,
            'success_rate': round(success_rate, 2),
            'total_repair_hours': round(self.total_repair_hours, 2),
            'emergency_responses': self.emergency_response_count,
            'pending_requests': len([r for r in self.maintenance_requests if r['status'] == 'pending']),
            'certifications_count': len(self.certifications),
            'technical_docs_authored': len(self.technical_docs),
            'avg_repair_time': round(self.total_repair_hours / total_maintenances, 2) if total_maintenances > 0 else 0
        }

        return metrics

    def get_assigned_machines_count(self):
        """Получить количество назначенных станков"""
        return len(self.machines)

    def __repr__(self):
        return f"Engineer(name='{self.name}', specialization='{self.specialization}', level={self.experience_level})"
