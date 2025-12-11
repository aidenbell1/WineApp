"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime, date, timedelta
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.models import Wine, Sale, Restaurant
from app.schemas.analytics import (
    TopBottomWines,
    WineSalesMetric,
    SalesTrendResponse,
    SalesTrend,
    InventoryHealth,
    ProfitAnalysis,
    DashboardSummary,
)

router = APIRouter()


@router.get("/dashboard/{restaurant_id}", response_model=DashboardSummary)
async def get_dashboard_summary(
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get overall dashboard summary for a restaurant
    """
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Date range for "last 30 days"
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Total wines
    total_wines = db.query(func.count(Wine.id)).filter(
        Wine.restaurant_id == restaurant_id
    ).scalar()
    
    # Total inventory
    total_bottles = db.query(func.sum(Wine.inventory_count)).filter(
        Wine.restaurant_id == restaurant_id
    ).scalar() or 0
    
    # Sales last 30 days
    sales_query = db.query(
        func.sum(Sale.quantity).label('total_sales'),
        func.sum(Sale.total_amount).label('total_revenue'),
        func.sum(Sale.quantity * (Sale.unit_price - Sale.unit_cost)).label('total_profit')
    ).filter(
        and_(
            Sale.restaurant_id == restaurant_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        )
    ).first()
    
    total_sales = sales_query.total_sales or 0
    revenue = sales_query.total_revenue or 0
    profit = sales_query.total_profit
    
    # Average profit margin
    if profit and revenue and revenue > 0:
        avg_profit_margin = (float(profit) / float(revenue)) * 100
    else:
        avg_profit_margin = None
    
    # Top wine this month
    top_wine_row = db.query(
        Wine.name,
        func.sum(Sale.quantity).label('sales_count')
    ).join(Sale).filter(
        and_(
            Sale.restaurant_id == restaurant_id,
            Sale.sale_date >= start_date
        )
    ).group_by(Wine.id, Wine.name).order_by(desc('sales_count')).first()
    
    top_wine = top_wine_row[0] if top_wine_row else None
    
    # Slowest wine (hasn't sold in 30+ days)
    slowest_wine_row = db.query(Wine.name, func.max(Sale.sale_date).label('last_sale'))\
        .outerjoin(Sale)\
        .filter(Wine.restaurant_id == restaurant_id)\
        .group_by(Wine.id, Wine.name)\
        .having(
            func.coalesce(func.max(Sale.sale_date), date(1900, 1, 1)) < start_date
        )\
        .first()
    
    slowest_wine = slowest_wine_row[0] if slowest_wine_row else None
    
    # Wines needing reorder (inventory < 5 and selling)
    wines_low_stock = db.query(func.count(Wine.id)).filter(
        and_(
            Wine.restaurant_id == restaurant_id,
            Wine.inventory_count < 5,
            Wine.times_sold > 0
        )
    ).scalar() or 0
    
    # Overstocked wines (inventory > 20 and not selling much)
    wines_overstocked = db.query(func.count(Wine.id)).filter(
        and_(
            Wine.restaurant_id == restaurant_id,
            Wine.inventory_count > 20,
            Wine.times_sold < 5
        )
    ).scalar() or 0
    
    return DashboardSummary(
        total_wines=total_wines,
        total_bottles_in_stock=int(total_bottles),
        total_sales_last_30_days=int(total_sales),
        revenue_last_30_days=revenue,
        profit_last_30_days=profit,
        avg_profit_margin=avg_profit_margin,
        top_wine_this_month=top_wine,
        slowest_wine=slowest_wine,
        wines_needing_reorder=wines_low_stock,
        overstocked_wines=wines_overstocked
    )


@router.get("/top-bottom-wines/{restaurant_id}", response_model=TopBottomWines)
async def get_top_bottom_wines(
    restaurant_id: UUID,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get top and bottom performing wines by sales volume
    """
    # Default to last 90 days if not specified
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=90)
    
    # Query for wine sales metrics
    wine_metrics = db.query(
        Wine.id,
        Wine.name,
        Wine.producer,
        Wine.vintage,
        func.sum(Sale.quantity).label('total_bottles_sold'),
        func.sum(Sale.total_amount).label('total_revenue'),
        func.sum(Sale.quantity * (Sale.unit_price - Sale.unit_cost)).label('total_profit'),
        func.avg(Sale.unit_price).label('avg_price'),
        func.max(Sale.sale_date).label('last_sale_date')
    ).join(Sale).filter(
        and_(
            Wine.restaurant_id == restaurant_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        )
    ).group_by(Wine.id, Wine.name, Wine.producer, Wine.vintage).all()
    
    # Convert to WineSalesMetric objects
    metrics = []
    for metric in wine_metrics:
        profit_margin = None
        if metric.total_profit and metric.total_revenue and metric.total_revenue > 0:
            profit_margin = (float(metric.total_profit) / float(metric.total_revenue)) * 100
        
        days_since_sale = None
        if metric.last_sale_date:
            days_since_sale = (end_date - metric.last_sale_date).days
        
        metrics.append(WineSalesMetric(
            wine_id=metric.id,
            wine_name=metric.name,
            producer=metric.producer,
            vintage=metric.vintage,
            total_bottles_sold=metric.total_bottles_sold,
            total_revenue=metric.total_revenue,
            total_profit=metric.total_profit,
            avg_price=metric.avg_price,
            profit_margin=profit_margin,
            last_sale_date=metric.last_sale_date,
            days_since_last_sale=days_since_sale
        ))
    
    # Sort by bottles sold
    metrics.sort(key=lambda x: x.total_bottles_sold, reverse=True)
    
    return TopBottomWines(
        top_sellers=metrics[:limit],
        slow_movers=metrics[-limit:] if len(metrics) > limit else []
    )


@router.get("/sales-trends/{restaurant_id}", response_model=SalesTrendResponse)
async def get_sales_trends(
    restaurant_id: UUID,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get sales trends over time (daily aggregation)
    """
    # Default to last 30 days
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Query daily sales
    daily_sales = db.query(
        Sale.sale_date,
        func.sum(Sale.quantity).label('total_sales'),
        func.sum(Sale.total_amount).label('total_revenue'),
        func.sum(Sale.quantity * (Sale.unit_price - Sale.unit_cost)).label('total_profit'),
        func.count(func.distinct(Sale.wine_id)).label('unique_wines_sold')
    ).filter(
        and_(
            Sale.restaurant_id == restaurant_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        )
    ).group_by(Sale.sale_date).order_by(Sale.sale_date).all()
    
    # Convert to SalesTrend objects
    trends = [
        SalesTrend(
            date=row.sale_date,
            total_sales=row.total_sales,
            total_revenue=row.total_revenue,
            total_profit=row.total_profit,
            unique_wines_sold=row.unique_wines_sold
        )
        for row in daily_sales
    ]
    
    # Calculate totals
    total_sales = sum(t.total_sales for t in trends)
    total_revenue = sum(t.total_revenue for t in trends)
    
    # Calculate average daily sales
    num_days = (end_date - start_date).days + 1
    avg_daily_sales = total_sales / num_days if num_days > 0 else 0
    
    return SalesTrendResponse(
        period_start=start_date,
        period_end=end_date,
        trends=trends,
        total_sales=total_sales,
        total_revenue=total_revenue,
        avg_daily_sales=avg_daily_sales
    )


@router.get("/inventory-health/{restaurant_id}", response_model=list[InventoryHealth])
async def get_inventory_health(
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Analyze inventory health and recommend actions
    """
    # Get wines with their sales velocity
    wines = db.query(Wine).filter(Wine.restaurant_id == restaurant_id).all()
    
    # Calculate sales velocity (last 30 days)
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    health_metrics = []
    
    for wine in wines:
        # Get sales count for last 30 days
        sales_count = db.query(func.sum(Sale.quantity)).filter(
            and_(
                Sale.wine_id == wine.id,
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            )
        ).scalar() or 0
        
        avg_daily_sales = float(sales_count) / 30.0
        
        # Calculate days until stockout
        days_until_stockout = None
        if avg_daily_sales > 0:
            days_until_stockout = int(wine.inventory_count / avg_daily_sales)
        
        # Determine if reorder needed (< 7 days of inventory)
        reorder_recommended = (
            days_until_stockout is not None and 
            days_until_stockout < 7 and 
            avg_daily_sales > 0
        )
        
        # Determine if overstocked (> 90 days of inventory or no sales)
        overstocked = (
            wine.inventory_count > 20 and 
            (avg_daily_sales == 0 or (days_until_stockout is not None and days_until_stockout > 90))
        )
        
        health_metrics.append(InventoryHealth(
            wine_id=wine.id,
            wine_name=wine.name,
            current_inventory=wine.inventory_count,
            avg_daily_sales=round(avg_daily_sales, 2),
            days_until_stockout=days_until_stockout,
            reorder_recommended=reorder_recommended,
            overstocked=overstocked
        ))
    
    # Sort by urgency (reorder recommended first, then by days until stockout)
    health_metrics.sort(
        key=lambda x: (
            not x.reorder_recommended,
            x.days_until_stockout if x.days_until_stockout is not None else 999
        )
    )
    
    return health_metrics


@router.get("/profit-analysis/{restaurant_id}", response_model=list[ProfitAnalysis])
async def get_profit_analysis(
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Analyze profit margins and provide pricing recommendations
    """
    # Get all wines with cost data
    wines = db.query(Wine).filter(
        and_(
            Wine.restaurant_id == restaurant_id,
            Wine.cost.isnot(None),
            Wine.cost > 0
        )
    ).all()
    
    # Calculate YTD profit for each wine
    year_start = date(date.today().year, 1, 1)
    
    profit_analyses = []
    
    for wine in wines:
        # Calculate profit per bottle
        profit_per_bottle = wine.price - wine.cost
        profit_margin = ((wine.price - wine.cost) / wine.price) * 100
        markup_percentage = ((wine.price - wine.cost) / wine.cost) * 100
        
        # Get YTD profit
        ytd_profit_query = db.query(
            func.sum(Sale.quantity * (Sale.unit_price - Sale.unit_cost)).label('total_profit')
        ).filter(
            and_(
                Sale.wine_id == wine.id,
                Sale.sale_date >= year_start
            )
        ).first()
        
        total_profit_ytd = ytd_profit_query.total_profit or 0
        
        # Simple pricing recommendation (aim for 60-70% margin)
        recommended_price = None
        if profit_margin < 60:
            # Recommend increasing price to hit 65% margin
            recommended_price = wine.cost / 0.35  # 35% COGS = 65% margin
        
        profit_analyses.append(ProfitAnalysis(
            wine_id=wine.id,
            wine_name=wine.name,
            cost=wine.cost,
            price=wine.price,
            profit_per_bottle=profit_per_bottle,
            profit_margin=round(profit_margin, 2),
            markup_percentage=round(markup_percentage, 2),
            total_profit_ytd=total_profit_ytd,
            recommended_price=round(recommended_price, 2) if recommended_price else None
        ))
    
    # Sort by profit margin (lowest first - need attention)
    profit_analyses.sort(key=lambda x: x.profit_margin)
    
    return profit_analyses
