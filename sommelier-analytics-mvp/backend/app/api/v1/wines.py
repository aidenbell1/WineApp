"""
Wine CRUD API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from uuid import UUID
import csv
import io

from app.core.database import get_db
from app.models import Wine, Restaurant
from app.schemas.wine import WineCreate, WineUpdate, WineResponse, WineListResponse

router = APIRouter()


@router.post("/", response_model=WineResponse, status_code=201)
async def create_wine(
    wine: WineCreate,
    db: Session = Depends(get_db)
):
    """Create a new wine"""
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == wine.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Create wine
    db_wine = Wine(**wine.model_dump())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    
    return db_wine


@router.get("/{wine_id}", response_model=WineResponse)
async def get_wine(
    wine_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific wine by ID"""
    wine = db.query(Wine).filter(Wine.id == wine_id).first()
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine


@router.get("/", response_model=WineListResponse)
async def list_wines(
    restaurant_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    wine_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List wines for a restaurant with pagination and filtering
    """
    # Base query
    query = db.query(Wine).filter(Wine.restaurant_id == restaurant_id)
    
    # Search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Wine.name.ilike(search_pattern),
                Wine.producer.ilike(search_pattern),
                Wine.varietal.ilike(search_pattern),
                Wine.region.ilike(search_pattern)
            )
        )
    
    # Type filter
    if wine_type:
        query = query.filter(Wine.wine_type == wine_type)
    
    # Get total count
    total = query.count()
    
    # Paginate
    offset = (page - 1) * page_size
    wines = query.offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size
    
    return WineListResponse(
        wines=wines,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.put("/{wine_id}", response_model=WineResponse)
async def update_wine(
    wine_id: UUID,
    wine_update: WineUpdate,
    db: Session = Depends(get_db)
):
    """Update a wine"""
    db_wine = db.query(Wine).filter(Wine.id == wine_id).first()
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    # Update only provided fields
    update_data = wine_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_wine, field, value)
    
    db.commit()
    db.refresh(db_wine)
    
    return db_wine


@router.delete("/{wine_id}", status_code=204)
async def delete_wine(
    wine_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a wine"""
    db_wine = db.query(Wine).filter(Wine.id == wine_id).first()
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    db.delete(db_wine)
    db.commit()
    
    return None


@router.post("/bulk-upload", status_code=201)
async def bulk_upload_wines(
    restaurant_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Bulk upload wines from CSV file
    
    Expected CSV format:
    name,producer,vintage,varietal,region,country,wine_type,body,price,cost,inventory_count
    """
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Read and parse CSV
    contents = await file.read()
    csv_reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    wines_created = 0
    errors = []
    
    for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (after header)
        try:
            # Create wine from row
            wine_data = {
                'restaurant_id': restaurant_id,
                'name': row.get('name'),
                'producer': row.get('producer') or None,
                'vintage': int(row['vintage']) if row.get('vintage') else None,
                'varietal': row.get('varietal') or None,
                'region': row.get('region') or None,
                'country': row.get('country') or None,
                'wine_type': row.get('wine_type') or None,
                'body': row.get('body') or None,
                'price': float(row['price']),
                'cost': float(row['cost']) if row.get('cost') else None,
                'inventory_count': int(row.get('inventory_count', 0)),
            }
            
            db_wine = Wine(**wine_data)
            db.add(db_wine)
            wines_created += 1
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    # Commit all wines
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    
    return {
        "message": f"Successfully uploaded {wines_created} wines",
        "wines_created": wines_created,
        "errors": errors if errors else None
    }
