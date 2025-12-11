"""
Dish model (for future pairing recommendations)
"""
from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Dish(Base):
    """Menu dish/item"""
    __tablename__ = "dishes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    
    # Basic info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # Appetizer, Entree, Dessert, etc.
    price = Column(Numeric(10, 2), nullable=True)
    
    # Dish characteristics (for pairing)
    main_protein = Column(String(100), nullable=True)  # Beef, Chicken, Fish, Vegetarian, etc.
    preparation_method = Column(String(100), nullable=True)  # Grilled, Roasted, Fried, etc.
    sauce_type = Column(String(100), nullable=True)  # Cream, Tomato, Wine-based, etc.
    spice_level = Column(String(20), nullable=True)  # Mild, Medium, Spicy
    
    # Menu status
    is_active = Column(Boolean, default=True)
    seasonal = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="dishes")
    
    def __repr__(self):
        return f"<Dish {self.name}>"
