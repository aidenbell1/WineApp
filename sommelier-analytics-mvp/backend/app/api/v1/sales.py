"""
Sales CRUD API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import date
from uuid import UUID
import csv
import io

from app.core.database import get_db
from app.models import Sale, Wine, Restaurant
from app.schemas.sale import SaleCreate, SaleResponse, SaleListResponse

router = APIRouter()


@router.post("/", response_model=SaleResponse, status_code=201)
async def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    """Create a new sale"""
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == sale.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Verify wine exists and belongs to restaurant
    wine = db.query(Wine).filter(
        and_(
            Wine.id == sale.wine_id,
            Wine.restaurant_id == sale.restaurant_id
        )
    ).first()
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found for this restaurant")
    
    # Calculate total amount
    total_amount = sale.unit_price * sale.quantity
    
    # Create sale
    db_sale = Sale(
        **sale.model_dump(),
        total_amount=total_amount
    )
    db.add(db_sale)
    
    # Update wine's times_sold counter
    wine.times_sold += sale.quantity
    
    # Optionally decrease inventory (if tracking)
    if wine.inventory_count >= sale.quantity:
        wine.inventory_count -= sale.quantity
    
    db.commit()
    db.refresh(db_sale)
    
    return db_sale


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific sale by ID"""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.get("/", response_model=SaleListResponse)
async def list_sales(
    restaurant_id: UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    wine_id: Optional[UUID] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List sales for a restaurant with filtering and pagination
    """
    # Base query
    query = db.query(Sale).filter(Sale.restaurant_id == restaurant_id)
    
    # Date filters
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    # Wine filter
    if wine_id:
        query = query.filter(Sale.wine_id == wine_id)
    
    # Order by most recent first
    query = query.order_by(Sale.sale_date.desc(), Sale.created_at.desc())
    
    # Get total count
    total = query.count()
    
    # Paginate
    offset = (page - 1) * page_size
    sales = query.offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size
    
    return SaleListResponse(
        sales=sales,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.delete("/{sale_id}", status_code=204)
async def delete_sale(
    sale_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a sale (and reverse inventory/stats)"""
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Get associated wine to update stats
    wine = db.query(Wine).filter(Wine.id == db_sale.wine_id).first()
    if wine:
        # Reverse the times_sold counter
        wine.times_sold = max(0, wine.times_sold - db_sale.quantity)
        # Restore inventory
        wine.inventory_count += db_sale.quantity
    
    db.delete(db_sale)
    db.commit()
    
    return None


@router.post("/bulk-upload", status_code=201)
async def bulk_upload_sales(
    restaurant_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Bulk upload sales from CSV file
    
    Expected CSV format:
    wine_name,sale_date,quantity,unit_price,unit_cost,server_name,table_number
    
    Note: wine_name must match exactly with a wine in the inventory
    """
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Get all wines for this restaurant (for lookup)
    wines = db.query(Wine).filter(Wine.restaurant_id == restaurant_id).all()
    wine_lookup = {wine.name.lower(): wine for wine in wines}
    
    # Read and parse CSV
    contents = await file.read()
    csv_reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    sales_created = 0
    errors = []
    
    for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (after header)
        try:
            # Look up wine by name
            wine_name = row.get('wine_name', '').strip()
            wine = wine_lookup.get(wine_name.lower())
            
            if not wine:
                errors.append(f"Row {row_num}: Wine '{wine_name}' not found in inventory")
                continue
            
            # Parse date
            from datetime import datetime
            sale_date = datetime.strptime(row['sale_date'], '%Y-%m-%d').date()
            
            # Parse numeric fields
            quantity = int(row['quantity'])
            unit_price = float(row['unit_price'])
            unit_cost = float(row['unit_cost']) if row.get('unit_cost') else None
            
            # Calculate total
            total_amount = unit_price * quantity
            
            # Create sale
            db_sale = Sale(
                restaurant_id=restaurant_id,
                wine_id=wine.id,
                sale_date=sale_date,
                quantity=quantity,
                unit_price=unit_price,
                unit_cost=unit_cost,
                total_amount=total_amount,
                server_name=row.get('server_name') or None,
                table_number=row.get('table_number') or None
            )
            db.add(db_sale)
            
            # Update wine stats
            wine.times_sold += quantity
            if wine.inventory_count >= quantity:
                wine.inventory_count -= quantity
            
            sales_created += 1
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    # Commit all sales
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    
    return {
        "message": f"Successfully uploaded {sales_created} sales",
        "sales_created": sales_created,
        "errors": errors if errors else None
    }
