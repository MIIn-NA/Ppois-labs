"""
Техническая документация - техническая документация
"""
from datetime import datetime
from typing import List


class TechnicalDocumentation:
    """Техническая документация"""

    def __init__(self, doc_id: str, title: str, doc_type: str):
        self.doc_id = doc_id
        self.title = title
        self.doc_type = doc_type  # manual, specification, blueprint, procedure
        self.products = []
        self.machines = []
        self.engineers = []
        self.product_specifications = []
        self.content = ""
        self.version = "1.0"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.author = None
        self.status = "draft"  # draft, review, approved, archived

    def add_product(self, product):
        """Добавить продукт"""
        self.products.append(product)

    def add_machine(self, machine):
        """Добавить станок"""
        self.machines.append(machine)

    def add_engineer(self, engineer):
        """Добавить инженера"""
        self.engineers.append(engineer)
        engineer.add_technical_documentation(self)

    def add_product_specification(self, spec):
        """Добавить спецификацию продукта"""
        self.product_specifications.append(spec)
        spec.add_technical_documentation(self)

    def set_content(self, content: str):
        """Установить содержание"""
        self.content = content
        self.updated_at = datetime.now()

    def set_author(self, author: str):
        """Установить автора"""
        self.author = author

    def update_version(self, new_version: str):
        """Обновить версию"""
        self.version = new_version
        self.updated_at = datetime.now()

    def submit_for_review(self):
        """Отправить на проверку"""
        self.status = "review"
        return {'doc': self.doc_id, 'submitted_at': datetime.now()}

    def approve(self):
        """Утвердить документ"""
        self.status = "approved"
        return {'doc': self.doc_id, 'approved_at': datetime.now()}

    def archive(self):
        """Архивировать документ"""
        self.status = "archived"
        return {'doc': self.doc_id, 'archived_at': datetime.now()}

    def is_approved(self):
        """Проверить, утвержден ли документ"""
        return self.status == "approved"

    def get_metadata(self):
        """Получить метаданные"""
        return {
            'doc_id': self.doc_id,
            'title': self.title,
            'type': self.doc_type,
            'version': self.version,
            'author': self.author,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"TechnicalDocumentation(title='{self.title}', type='{self.doc_type}', version='{self.version}')"
