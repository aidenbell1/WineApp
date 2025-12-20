"""
Sale model for tracking wine sales
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Sale(Base):
    """Wine sale transaction"""
    __tablename__ = "sales"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    wine_id = Column(UUID(as_uuid=True), ForeignKey("wines.id"), nullable=False)
    
    # Sale details
    sale_date = Column(Date, nullable=False)  # Date of sale (not datetime for easier aggregation)
    quantity = Column(Integer, default=1, nullable=False)  # Bottles/glasses sold
    unit_price = Column(Numeric(10, 2), nullable=False)  # Price per unit at time of sale
    total_amount = Column(Numeric(10, 2), nullable=False)  # quantity * unit_price
    
    # Cost tracking (snapshot at time of sale)
    unit_cost = Column(Numeric(10, 2), nullable=True)  # Cost per unit at time of sale
    
    # Optional metadata
    server_name = Column(String(100), nullable=True)
    table_number = Column(String(20), nullable=True)
    notes = Column(String(500), nullable=True)
    
    # POS integration (for future)
    pos_transaction_id = Column(String(100), nullable=True, unique=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="sales")
    wine = relationship("Wine", back_populates="sales")
    
    @property
    def profit(self):
        """Calculate profit for this sale"""
        if self.unit_cost is not 0:
            return (self.unit_price - self.unit_cost) * self.quantity
        return None
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.unit_cost is not 0 and self.unit_price is not 0:
            return ((self.unit_price - self.unit_cost) / self.unit_price) * 100
        return None
    
    def __repr__(self):
        return f"<Sale {self.wine_id} on {self.sale_date}>"
