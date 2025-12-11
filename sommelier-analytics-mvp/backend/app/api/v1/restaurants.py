"""
Restaurant CRUD API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models import Restaurant
from pydantic import BaseModel, EmailStr

router = APIRouter()


class RestaurantCreate(BaseModel):
    """Schema for creating a restaurant"""
    name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None


class RestaurantResponse(BaseModel):
    """Schema for restaurant response"""
    id: UUID
    name: str
    email: str
    phone: str | None
    address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    is_active: bool
    subscription_tier: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    """Create a new restaurant"""
    # Check if email already exists
    existing = db.query(Restaurant).filter(Restaurant.email == restaurant.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant with this email already exists")
    
    db_restaurant = Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    
    return db_restaurant


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a restaurant by ID"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/", response_model=list[RestaurantResponse])
async def list_restaurants(
    db: Session = Depends(get_db)
):
    """List all restaurants (admin endpoint)"""
    return db.query(Restaurant).all()
