"""
Инспектор качества - проверяет качество продукции
"""
from datetime import datetime, timedelta
from typing import List, Dict
import random


class QualityInspector:
    """Инспектор качества"""

    def __init__(self, name: str, employee_id: str, salary: float):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.department = None
        self.quality_control = None
        self.inspected_products = []
        self.defect_reports = []
        self.approved_batches = []
        self.rejected_batches = []
        self.hire_date = datetime.now()
        self.is_active = True
        self.position = "Quality Inspector"
        self.certifications = []
        self.inspection_level = 1  # 1-5
        self.total_passed = 0
        self.total_failed = 0
        self.false_positives = 0  # Ошибочно забракованные
        self.false_negatives = 0  # Пропущенные дефекты

    def assign_to_quality_control(self, quality_control):
        """
        Назначить в отдел контроля качества

        Регистрирует инспектора в системе QC
        """
        if not self.is_active:
            raise RuntimeError(f"Cannot assign inactive inspector {self.name}")

        self.quality_control = quality_control

        print(f"Quality Inspector {self.name} assigned to Quality Control")

        return quality_control

    def inspect_product(self, product, inspection_type: str = "standard"):
        """
        Проверить продукт с детальной оценкой

        Выполняет многоуровневую проверку и выставляет оценку качества
        """
        if not self.is_active:
            raise RuntimeError("Inactive inspector cannot perform inspections")

        if not self.quality_control:
            print(f"Warning: Inspector {self.name} is not assigned to Quality Control department")

        # Определение критериев проверки
        inspection_criteria = self._get_inspection_criteria(inspection_type)

        # Симуляция проверки - выставление оценок по каждому критерию
        scores = {}
        total_score = 0

        for criterion, weight in inspection_criteria.items():
            # Базовая оценка зависит от уровня инспектора
            base_score = random.uniform(70, 100)
            inspector_bonus = self.inspection_level * 2
            criterion_score = min(100, base_score + inspector_bonus)

            scores[criterion] = round(criterion_score, 2)
            total_score += criterion_score * weight

        # Определение статуса
        if total_score >= 90:
            status = 'passed'
            self.total_passed += 1
        elif total_score >= 70:
            status = 'needs_review'
        else:
            status = 'failed'
            self.total_failed += 1

        inspection_result = {
            'inspection_id': f"INS-{len(self.inspected_products) + 1:06d}",
            'product': product.name if hasattr(product, 'name') else str(product),
            'inspector': self.name,
            'timestamp': datetime.now(),
            'type': inspection_type,
            'status': status,
            'total_score': round(total_score, 2),
            'criteria_scores': scores,
            'notes': self._generate_inspection_notes(status, total_score)
        }

        self.inspected_products.append(inspection_result)

        # Автоматическое создание отчета о дефектах при провале
        if status == 'failed':
            defects = self._identify_defects(scores)
            self.create_defect_report(product, defects)

        print(f"[{self.name}] Inspection complete: {inspection_result['product']}")
        print(f"Status: {status} | Score: {total_score:.2f}/100")

        return inspection_result

    def _get_inspection_criteria(self, inspection_type: str) -> Dict[str, float]:
        """Получить критерии проверки в зависимости от типа"""
        criteria = {
            "standard": {
                "visual_quality": 0.3,
                "dimensional_accuracy": 0.3,
                "functional_test": 0.4
            },
            "detailed": {
                "visual_quality": 0.2,
                "dimensional_accuracy": 0.2,
                "functional_test": 0.3,
                "material_quality": 0.15,
                "durability_test": 0.15
            },
            "quick": {
                "visual_quality": 0.5,
                "functional_test": 0.5
            }
        }

        return criteria.get(inspection_type, criteria["standard"])

    def _generate_inspection_notes(self, status: str, score: float) -> str:
        """Генерировать заметки на основе результата"""
        if status == 'passed':
            return f"Product meets all quality standards. Excellent score: {score:.1f}"
        elif status == 'needs_review':
            return f"Product requires additional review. Score: {score:.1f}"
        else:
            return f"Product failed quality inspection. Multiple defects found. Score: {score:.1f}"

    def _identify_defects(self, scores: Dict[str, float]) -> str:
        """Определить дефекты на основе низких оценок"""
        defects = []

        for criterion, score in scores.items():
            if score < 70:
                defects.append(f"{criterion.replace('_', ' ').title()}: {score:.1f}/100")

        return "; ".join(defects) if defects else "General quality issues"

    def create_defect_report(self, product, defect_description: str, severity: str = "medium"):
        """
        Создать детальный отчет о дефекте

        Классифицирует дефект и рекомендует действия
        """
        if severity not in ["low", "medium", "high", "critical"]:
            raise ValueError("Severity must be 'low', 'medium', 'high', or 'critical'")

        report = {
            'report_id': f"DEF-{len(self.defect_reports) + 1:05d}",
            'product': product.name if hasattr(product, 'name') else str(product),
            'defect': defect_description,
            'severity': severity,
            'inspector': self.name,
            'timestamp': datetime.now(),
            'recommended_action': self._recommend_defect_action(severity),
            'requires_rework': severity in ["medium", "high"],
            'requires_scrap': severity == "critical"
        }

        self.defect_reports.append(report)

        # Уведомление при критических дефектах
        if severity == "critical":
            print(f"CRITICAL DEFECT DETECTED: {defect_description}")
            print(f"Product: {report['product']} | Inspector: {self.name}")

        print(f"Defect report created: {report['report_id']} (Severity: {severity})")

        return report

    def _recommend_defect_action(self, severity: str) -> str:
        """Рекомендовать действия на основе серьезности дефекта"""
        actions = {
            "low": "minor_rework",
            "medium": "rework_and_reinspect",
            "high": "major_rework_or_scrap",
            "critical": "immediate_scrap_and_investigation"
        }
        return actions.get(severity, "rework_and_reinspect")

    def approve_batch(self, batch, batch_size: int):
        """
        Утвердить партию с статистической проверкой

        Использует выборочный контроль для больших партий
        """
        if not self.is_active:
            raise RuntimeError("Inactive inspector cannot approve batches")

        # Определение размера выборки (от 10% до 100% в зависимости от размера)
        sample_size = min(batch_size, max(10, int(batch_size * 0.1)))

        # Симуляция проверки выборки
        inspection_accuracy = min(0.95, 0.7 + (self.inspection_level * 0.05))
        defects_in_sample = 0

        for _ in range(sample_size):
            # Вероятность дефекта в выборке
            if random.random() > inspection_accuracy:
                defects_in_sample += 1

        # Критерий приемки: не более 5% дефектов в выборке
        defect_rate = (defects_in_sample / sample_size) * 100
        is_approved = defect_rate <= 5.0

        batch_result = {
            'batch_id': batch.batch_id if hasattr(batch, 'batch_id') else str(batch),
            'batch_size': batch_size,
            'sample_size': sample_size,
            'defects_found': defects_in_sample,
            'defect_rate': round(defect_rate, 2),
            'inspector': self.name,
            'approved': is_approved,
            'timestamp': datetime.now(),
            'certification_number': f"CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}" if is_approved else None
        }

        if is_approved:
            self.approved_batches.append(batch_result)
            print(f"Batch APPROVED: {batch_result['batch_id']}")
            print(f"Sample: {sample_size}/{batch_size} | Defect rate: {defect_rate:.2f}%")
        else:
            self.rejected_batches.append(batch_result)
            print(f"Batch REJECTED: {batch_result['batch_id']}")
            print(f"Defect rate ({defect_rate:.2f}%) exceeds acceptable limit (5.00%)")

        return batch_result

    def reject_batch(self, batch, reason: str):
        """
        Отклонить партию с указанием причины

        Создает запись об отклонении для дальнейшего анализа
        """
        rejection = {
            'batch_id': batch.batch_id if hasattr(batch, 'batch_id') else str(batch),
            'inspector': self.name,
            'reason': reason,
            'timestamp': datetime.now(),
            'requires_investigation': True
        }

        self.rejected_batches.append(rejection)

        print(f"Batch {rejection['batch_id']} REJECTED by {self.name}")
        print(f"Reason: {reason}")

        return rejection

    def add_certification(self, cert_name: str, issuing_body: str):
        """Добавить сертификацию инспектору"""
        cert = {
            'name': cert_name,
            'issuing_body': issuing_body,
            'date_obtained': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=1095)  # 3 года
        }

        self.certifications.append(cert)

        print(f"Certification added for {self.name}: {cert_name}")

        return cert

    def increase_inspection_level(self):
        """
        Повысить уровень инспекции

        Требует минимального количества проверок
        """
        if self.inspection_level >= 5:
            print(f"Inspector {self.name} is already at maximum inspection level")
            return False

        total_inspections = len(self.inspected_products)
        required_inspections = self.inspection_level * 100

        if total_inspections < required_inspections:
            raise ValueError(
                f"Insufficient inspections: {total_inspections}/{required_inspections}"
            )

        # Проверка точности (не более 10% ошибок)
        error_rate = ((self.false_positives + self.false_negatives) / total_inspections * 100) if total_inspections > 0 else 0

        if error_rate > 10:
            raise ValueError(
                f"Error rate too high: {error_rate:.2f}%. Must be below 10% for promotion."
            )

        self.inspection_level += 1
        self.salary *= 1.10  # 10% повышение зарплаты

        print(f"Inspector {self.name} promoted to inspection level {self.inspection_level}")
        print(f"New salary: {self.salary:.2f}")

        return True

    def get_inspection_count(self):
        """Получить количество проверок"""
        return len(self.inspected_products)

    def get_defect_rate(self):
        """Получить процент дефектов"""
        if not self.inspected_products:
            return 0.0

        failed_count = sum(1 for insp in self.inspected_products if insp['status'] == 'failed')
        return round((failed_count / len(self.inspected_products)) * 100, 2)

    def get_performance_statistics(self) -> Dict:
        """
        Получить статистику производительности инспектора

        Возвращает детальные метрики работы
        """
        total_inspections = len(self.inspected_products)
        pass_rate = (self.total_passed / total_inspections * 100) if total_inspections > 0 else 0

        stats = {
            'name': self.name,
            'inspection_level': self.inspection_level,
            'total_inspections': total_inspections,
            'total_passed': self.total_passed,
            'total_failed': self.total_failed,
            'pass_rate': round(pass_rate, 2),
            'defect_rate': self.get_defect_rate(),
            'defect_reports_created': len(self.defect_reports),
            'batches_approved': len(self.approved_batches),
            'batches_rejected': len(self.rejected_batches),
            'batch_approval_rate': round(
                (len(self.approved_batches) / (len(self.approved_batches) + len(self.rejected_batches)) * 100)
                if (len(self.approved_batches) + len(self.rejected_batches)) > 0 else 0, 2
            ),
            'certifications_count': len(self.certifications),
            'false_positive_rate': round((self.false_positives / total_inspections * 100) if total_inspections > 0 else 0, 2),
            'false_negative_rate': round((self.false_negatives / total_inspections * 100) if total_inspections > 0 else 0, 2)
        }

        return stats

    def __repr__(self):
        return f"QualityInspector(name='{self.name}', level={self.inspection_level}, inspections={len(self.inspected_products)})"
