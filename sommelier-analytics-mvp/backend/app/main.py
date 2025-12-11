"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import restaurants, wines, sales, analytics
from app.core.config import settings

app = FastAPI(
    title="Sommelier Analytics API",
    description="Wine sales analytics for restaurants",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(restaurants.router, prefix="/api/v1/restaurants", tags=["restaurants"])
app.include_router(wines.router, prefix="/api/v1/wines", tags=["wines"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Sommelier Analytics API",
        "version": "0.1.0",
        "status": "healthy"
    }


@app.get("/health")
async def health():
    """Health check for load balancers"""
    return {"status": "healthy"}
