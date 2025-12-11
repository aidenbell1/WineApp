"""
Models package - exports all database models
"""
from app.models.restaurant import Restaurant
from app.models.wine import Wine, WineBody, WineType
from app.models.sale import Sale
from app.models.dish import Dish

__all__ = [
    "Restaurant",
    "Wine",
    "WineBody",
    "WineType",
    "Sale",
    "Dish",
]
