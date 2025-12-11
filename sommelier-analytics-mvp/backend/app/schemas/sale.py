"""
Sale schemas for API validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal


class SaleBase(BaseModel):
    """Base sale schema"""
    wine_id: UUID
    sale_date: date
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    unit_cost: Optional[Decimal] = Field(None, ge=0)
    
    server_name: Optional[str] = Field(None, max_length=100)
    table_number: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)


class SaleCreate(SaleBase):
    """Schema for creating a new sale"""
    restaurant_id: UUID
    
    @property
    def total_amount(self) -> Decimal:
        return self.unit_price * self.quantity


class SaleBulkCreate(BaseModel):
    """Schema for bulk creating sales (CSV upload)"""
    restaurant_id: UUID
    sales: list[SaleBase]


class SaleResponse(SaleBase):
    """Schema for sale response"""
    id: UUID
    restaurant_id: UUID
    total_amount: Decimal
    profit: Optional[Decimal] = None
    profit_margin: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class SaleListResponse(BaseModel):
    """Schema for paginated sale list"""
    sales: list[SaleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
