"""
Wine model
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.core.database import Base


class WineBody(str, enum.Enum):
    """Wine body enumeration"""
    LIGHT = "light"
    MEDIUM = "medium"
    FULL = "full"


class WineType(str, enum.Enum):
    """Wine type enumeration"""
    RED = "red"
    WHITE = "white"
    ROSE = "rose"
    SPARKLING = "sparkling"
    DESSERT = "dessert"
    FORTIFIED = "fortified"


class Wine(Base):
    """Wine inventory item"""
    __tablename__ = "wines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    
    # Basic info
    name = Column(String(255), nullable=False)
    producer = Column(String(255), nullable=True)
    vintage = Column(Integer, nullable=True)  # Year, e.g., 2019
    varietal = Column(String(100), nullable=True)  # Pinot Noir, Chardonnay, etc.
    region = Column(String(255), nullable=True)  # Burgundy, Napa Valley, etc.
    country = Column(String(100), nullable=True)
    
    # Wine characteristics
    wine_type = Column(SQLEnum(WineType), nullable=True)
    body = Column(SQLEnum(WineBody), nullable=True)
    sweetness = Column(Integer, nullable=True)  # 1-5 scale (1=dry, 5=sweet)
    acidity = Column(Integer, nullable=True)  # 1-5 scale
    tannin = Column(Integer, nullable=True)  # 1-5 scale (reds only)
    alcohol_content = Column(Numeric(4, 2), nullable=True)  # e.g., 13.5%
    
    # Business data
    cost = Column(Numeric(10, 2), nullable=True)  # What restaurant pays
    price = Column(Numeric(10, 2), nullable=False)  # Menu price
    inventory_count = Column(Integer, default=0)  # Current bottles in stock
    
    # Additional details
    tasting_notes = Column(Text, nullable=True)
    bottle_size = Column(String(20), default="750ml")  # 750ml, 1.5L, etc.
    sku = Column(String(100), nullable=True)  # Internal SKU
    
    # Analytics (computed)
    times_sold = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="wines")
    sales = relationship("Sale", back_populates="wine", cascade="all, delete-orphan")
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost is not 0 and self.price is not 0:
            return ((self.price - self.cost) / self.price) * 100
        return None
    
    @property
    def markup(self):
        """Calculate markup percentage"""
        if self.cost is not 0 and self.price is not 0:
            return ((self.price - self.cost) / self.cost) * 100
        return None
    
    def __repr__(self):
        return f"<Wine {self.name} ({self.vintage})>"
