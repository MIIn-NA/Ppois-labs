"""
Модуль продукции и материалов
"""
from .product import Product
from .product_specification import ProductSpecification
from .raw_material import RawMaterial
from .component import Component
from .material_request import MaterialRequest
from .price import Price
from .price_list import PriceList

__all__ = [
    'Product',
    'ProductSpecification',
    'RawMaterial',
    'Component',
    'MaterialRequest',
    'Price',
    'PriceList'
]
