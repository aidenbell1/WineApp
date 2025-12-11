"""
Wine schemas for API validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class WineBase(BaseModel):
    """Base wine schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    producer: Optional[str] = Field(None, max_length=255)
    vintage: Optional[int] = Field(None, ge=1900, le=2030)
    varietal: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    
    wine_type: Optional[str] = Field(None, pattern="^(red|white|rose|sparkling|dessert|fortified)$")
    body: Optional[str] = Field(None, pattern="^(light|medium|full)$")
    sweetness: Optional[int] = Field(None, ge=1, le=5)
    acidity: Optional[int] = Field(None, ge=1, le=5)
    tannin: Optional[int] = Field(None, ge=1, le=5)
    alcohol_content: Optional[Decimal] = Field(None, ge=0, le=20)
    
    price: Decimal = Field(..., gt=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    inventory_count: int = Field(default=0, ge=0)
    
    tasting_notes: Optional[str] = None
    bottle_size: str = Field(default="750ml")
    sku: Optional[str] = Field(None, max_length=100)


class WineCreate(WineBase):
    """Schema for creating a new wine"""
    restaurant_id: UUID
    
    @field_validator('cost')
    @classmethod
    def cost_must_be_less_than_price(cls, v, info):
        if v is not None and 'price' in info.data and v >= info.data['price']:
            raise ValueError('Cost must be less than price')
        return v


class WineUpdate(BaseModel):
    """Schema for updating a wine (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    producer: Optional[str] = Field(None, max_length=255)
    vintage: Optional[int] = Field(None, ge=1900, le=2030)
    varietal: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    
    wine_type: Optional[str] = Field(None, pattern="^(red|white|rose|sparkling|dessert|fortified)$")
    body: Optional[str] = Field(None, pattern="^(light|medium|full)$")
    sweetness: Optional[int] = Field(None, ge=1, le=5)
    acidity: Optional[int] = Field(None, ge=1, le=5)
    tannin: Optional[int] = Field(None, ge=1, le=5)
    alcohol_content: Optional[Decimal] = Field(None, ge=0, le=20)
    
    price: Optional[Decimal] = Field(None, gt=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    inventory_count: Optional[int] = Field(None, ge=0)
    
    tasting_notes: Optional[str] = None
    bottle_size: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)


class WineResponse(WineBase):
    """Schema for wine response (includes computed fields)"""
    id: UUID
    restaurant_id: UUID
    times_sold: int
    created_at: datetime
    updated_at: datetime
    profit_margin: Optional[float] = None
    markup: Optional[float] = None
    
    class Config:
        from_attributes = True


class WineListResponse(BaseModel):
    """Schema for paginated wine list"""
    wines: list[WineResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
