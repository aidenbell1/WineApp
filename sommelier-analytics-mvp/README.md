# 🍷 Sommelier Analytics MVP

> **Wine Sales Analytics Dashboard for Restaurants**
> 
> Help restaurant managers make data-driven decisions about their wine programs without hiring a sommelier.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com)

---

## 🎯 What Is This?

A complete backend analytics platform that helps restaurants:
- 📊 Track which wines are selling (and which aren't)
- 💰 Analyze profit margins and optimize pricing
- 📦 Monitor inventory and prevent stockouts
- 📈 Visualize sales trends over time
- 🎯 Get actionable recommendations

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

```bash
./setup.sh
```

### Option 2: Manual Setup

```bash
# 1. Start services
docker-compose up -d

# 2. Run migrations
docker-compose exec backend alembic upgrade head

# 3. Open API docs
open http://localhost:8000/docs
```

---

## 🎨 What's Included

### ✅ Core Features (Production-Ready)
- [x] Restaurant management (multi-tenant ready)
- [x] Wine inventory CRUD with search & filters
- [x] Sales transaction tracking
- [x] CSV bulk import (wines & sales)
- [x] Dashboard summary metrics
- [x] Top/bottom seller analysis
- [x] Sales trend charts (time series)
- [x] Inventory health monitoring
- [x] Profit margin analysis
- [x] Pricing recommendations
- [x] Date range filtering
- [x] Pagination & search
- [x] Auto-generated API documentation

### 🚧 Coming Soon
- [ ] Next.js frontend dashboard
- [ ] Authentication (Auth0)
- [ ] Multi-user support
- [ ] Claude AI pairing recommendations
- [ ] Server mobile app (React Native)
- [ ] POS integrations (Toast, Square)

---

## 🏗️ Tech Stack

```
Backend:      FastAPI (Python) - Fast, modern, type-safe
Database:     PostgreSQL 15 - ACID compliance, full-text search
ORM:          SQLAlchemy - Type-safe queries, migrations
Validation:   Pydantic - Request/response validation
Migrations:   Alembic - Database version control
Container:    Docker - Consistent environments
```

---

## 📊 Example Usage

### Create a Restaurant
```bash
curl -X POST http://localhost:8000/api/v1/restaurants/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Wine Bar","email":"test@example.com"}'
```

### Upload Wine Inventory (CSV)
```bash
curl -X POST "http://localhost:8000/api/v1/wines/bulk-upload?restaurant_id=<ID>" \
  -F "file=@sample-data/wines_template.csv"
```

### Get Analytics Dashboard
```bash
curl http://localhost:8000/api/v1/analytics/dashboard/<RESTAURANT_ID>
```

**Response:**
```json
{
  "total_wines": 8,
  "total_bottles_in_stock": 147,
  "total_sales_last_30_days": 10,
  "revenue_last_30_days": 641.00,
  "profit_last_30_days": 320.00,
  "avg_profit_margin": 49.92,
  "top_wine_this_month": "2022 Whispering Angel Rosé",
  "slowest_wine": "2020 Château Margaux",
  "wines_needing_reorder": 2,
  "overstocked_wines": 1
}
```

---

## 🔌 Key API Endpoints

### Analytics (The Core Value) ⭐
```
GET /api/v1/analytics/dashboard/{id}          Dashboard summary
GET /api/v1/analytics/top-bottom-wines/{id}   Top/bottom sellers
GET /api/v1/analytics/sales-trends/{id}       Time series data
GET /api/v1/analytics/inventory-health/{id}   Reorder alerts
GET /api/v1/analytics/profit-analysis/{id}    Margin analysis
```

### Data Management
```
POST /api/v1/restaurants/              Create restaurant
POST /api/v1/wines/bulk-upload         Upload wines CSV
POST /api/v1/sales/bulk-upload         Upload sales CSV
GET  /api/v1/wines/?restaurant_id=...  List wines (paginated)
GET  /api/v1/sales/?restaurant_id=...  List sales (filtered)
```

**Full API Reference**: http://localhost:8000/docs
