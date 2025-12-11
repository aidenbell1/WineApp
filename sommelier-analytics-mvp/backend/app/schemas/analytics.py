"""
Analytics schemas for dashboard data
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from uuid import UUID
from decimal import Decimal


class WineSalesMetric(BaseModel):
    """Wine sales performance metrics"""
    wine_id: UUID
    wine_name: str
    producer: Optional[str]
    vintage: Optional[int]
    
    total_bottles_sold: int
    total_revenue: Decimal
    total_profit: Optional[Decimal]
    avg_price: Decimal
    profit_margin: Optional[float]
    
    last_sale_date: Optional[date]
    days_since_last_sale: Optional[int]


class TopBottomWines(BaseModel):
    """Top and bottom performing wines"""
    top_sellers: List[WineSalesMetric]
    slow_movers: List[WineSalesMetric]


class SalesTrend(BaseModel):
    """Sales trend data point"""
    date: date
    total_sales: int
    total_revenue: Decimal
    total_profit: Optional[Decimal]
    unique_wines_sold: int


class SalesTrendResponse(BaseModel):
    """Time series of sales trends"""
    period_start: date
    period_end: date
    trends: List[SalesTrend]
    total_sales: int
    total_revenue: Decimal
    avg_daily_sales: float


class InventoryHealth(BaseModel):
    """Inventory health metrics"""
    wine_id: UUID
    wine_name: str
    current_inventory: int
    avg_daily_sales: float
    days_until_stockout: Optional[int]  # None if not selling
    reorder_recommended: bool
    overstocked: bool


class ProfitAnalysis(BaseModel):
    """Profit analysis by wine"""
    wine_id: UUID
    wine_name: str
    cost: Decimal
    price: Decimal
    profit_per_bottle: Decimal
    profit_margin: float
    markup_percentage: float
    total_profit_ytd: Decimal
    recommended_price: Optional[Decimal] = None  # Based on market analysis


class DashboardSummary(BaseModel):
    """Overall dashboard summary"""
    total_wines: int
    total_bottles_in_stock: int
    total_sales_last_30_days: int
    revenue_last_30_days: Decimal
    profit_last_30_days: Optional[Decimal]
    avg_profit_margin: Optional[float]
    
    top_wine_this_month: Optional[str]
    slowest_wine: Optional[str]
    wines_needing_reorder: int
    overstocked_wines: int


class DateRangeFilter(BaseModel):
    """Common date range filter"""
    start_date: date
    end_date: date
