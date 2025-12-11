# Development Guide

## Project Overview

This is the **Wine Sales Analytics Dashboard MVP** - the first feature of the Sommelier AI platform.

**Goal**: Help restaurant managers understand their wine sales performance and make data-driven decisions.

---

## Architecture

```
Frontend (Next.js)          Backend (FastAPI)           Database (PostgreSQL)
     │                            │                           │
     │─── HTTP/REST ───>          │                           │
     │                            │──── SQLAlchemy ORM ───>   │
     │<─── JSON data ────         │                           │
                                  │<──── Query results ───    │
```

### Tech Stack Decisions

**Why FastAPI?**
- Native async support (handles concurrent requests well)
- Auto-generated API docs (Swagger/OpenAPI)
- Type hints everywhere (catches bugs early)
- Fast development with Pydantic validation

**Why PostgreSQL?**
- ACID compliance (important for money/sales data)
- Great for relational data (wines → sales → restaurants)
- Full-text search built-in
- Can add pgvector later for AI features

**Why SQLAlchemy ORM?**
- Type-safe database queries
- Migration management with Alembic
- Easier to work with than raw SQL for most queries

---

## Database Schema

### Tables

**restaurants**
- Core entity representing a customer
- Tracks subscription status
- One restaurant → many wines, sales, dishes

**wines**
- Wine inventory for a restaurant
- Includes tasting profile (body, acidity, etc.)
- Tracks inventory count and sales statistics

**sales**
- Transactional records of wine sales
- Captures price/cost at time of sale
- Links to specific wine and restaurant

**dishes**
- Menu items (for future pairing feature)
- Not used in MVP but schema is ready

### Key Indexes
- `restaurant_id` on wines, sales, dishes (fast filtering)
- `sale_date` on sales (fast date range queries)
- `name` on wines (fast search)

---

## API Design Patterns

### RESTful Conventions
- `GET /api/v1/wines/` - List wines (paginated)
- `GET /api/v1/wines/{id}` - Get single wine
- `POST /api/v1/wines/` - Create wine
- `PUT /api/v1/wines/{id}` - Update wine
- `DELETE /api/v1/wines/{id}` - Delete wine

### Analytics Endpoints
- Read-only (GET only)
- Accept date range filters
- Return aggregated/computed data
- Performance-optimized queries

### Response Patterns
```json
{
  "wines": [...],
  "total": 150,
  "page": 1,
  "page_size": 50,
  "total_pages": 3
}
```

All list endpoints return this pagination structure.

---

## Key Features Implemented

### ✅ Phase 1: Core Analytics

1. **Dashboard Summary**
   - Total inventory count
   - Sales metrics (30 days)
   - Top/slowest wines
   - Inventory alerts

2. **Top/Bottom Wines**
   - Ranked by sales volume
   - Profit margins
   - Last sale date

3. **Sales Trends**
   - Daily time series
   - Revenue tracking
   - Profit calculation

4. **Inventory Health**
   - Days until stockout
   - Reorder recommendations
   - Overstocked items

5. **Profit Analysis**
   - Margin percentages
   - Pricing recommendations
   - YTD profit per wine

### CSV Upload Support
- Bulk wine import
- Bulk sales import
- Error handling with row-level feedback

---

## Development Workflows

### Adding a New Endpoint

1. **Create the schema** (`app/schemas/`)
```python
class MyNewSchema(BaseModel):
    field1: str
    field2: int
```

2. **Add the endpoint** (`app/api/v1/my_endpoint.py`)
```python
@router.get("/my-endpoint")
async def my_endpoint(db: Session = Depends(get_db)):
    # Query logic here
    return {"data": "result"}
```

3. **Register the router** (`app/main.py`)
```python
app.include_router(my_endpoint.router, prefix="/api/v1/my-endpoint", tags=["my-endpoint"])
```

4. **Test it**
- Go to http://localhost:8000/docs
- Your endpoint will be there automatically

### Adding a Database Column

1. **Update the model** (`app/models/wine.py`)
```python
new_field = Column(String(100), nullable=True)
```

2. **Generate migration**
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add new_field to wines"
```

3. **Review the migration** (in `alembic/versions/`)
4. **Apply it**
```bash
docker-compose exec backend alembic upgrade head
```

### Writing Tests

```python
# tests/test_analytics.py
def test_dashboard_summary(client, db_session):
    # Create test data
    restaurant = create_restaurant(db_session)
    wine = create_wine(db_session, restaurant.id)
    
    # Make request
    response = client.get(f"/api/v1/analytics/dashboard/{restaurant.id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["total_wines"] == 1
```

Run tests:
```bash
docker-compose exec backend pytest
```

---

## Performance Considerations

### Database Query Optimization

**Good** (uses indexes):
```python
wines = db.query(Wine).filter(Wine.restaurant_id == restaurant_id).all()
```

**Bad** (loads everything):
```python
wines = db.query(Wine).all()
wines_filtered = [w for w in wines if w.restaurant_id == restaurant_id]
```

### Pagination Best Practices
- Always paginate list endpoints
- Default page_size: 50
- Max page_size: 100
- Use offset/limit in SQL

### Analytics Query Tips
- Use `func.sum()`, `func.count()` for aggregations
- Group by date for time series
- Index date columns used in filters
- Consider caching for expensive queries

---

## Security Best Practices

### Current MVP (No Auth)
- Single-tenant demo mode
- Anyone with restaurant_id can access data
- **Not production-ready**

### Future Auth Implementation
```python
# Add to dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate JWT token
    # Return user object
    pass

# Protect endpoints
@router.get("/wines/")
async def list_wines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify user has access to this restaurant
    # Return data
```

### Environment Variables
- Never commit `.env` file
- Use `.env.example` as template
- Rotate SECRET_KEY in production

---

## Common Issues & Solutions

### Issue: Migration conflicts
```bash
# Reset migrations (⚠️ loses data)
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head
```

### Issue: Circular imports
- Keep imports at file level
- Use `from __future__ import annotations` for type hints
- Import models in dependencies, not at module level

### Issue: Decimal vs Float
- Use `Decimal` for money (accurate)
- PostgreSQL `Numeric` → SQLAlchemy `Decimal`
- Convert to `float` for JSON serialization if needed

### Issue: UUID types
- Always use `UUID(as_uuid=True)` in SQLAlchemy
- Pydantic accepts string UUIDs automatically
- PostgreSQL stores as native UUID (fast)

---

## Next Features to Build

### Week 3-4: Frontend Dashboard

**Priority 1: Dashboard View**
- Cards showing key metrics
- Charts for sales trends (Recharts)
- Table of top/bottom wines

**Priority 2: Inventory Management**
- List view with search/filter
- Add/edit wines manually
- CSV import interface

**Priority 3: Sales View**
- Sales history table
- Filters by date, wine, server
- CSV import interface

### Week 5-6: Insights & Recommendations

**Priority 1: Rule-Based Recommendations**
- "Low inventory" alerts
- "Overpriced" wine detection
- "Slow mover" recommendations

**Priority 2: Pairing Suggestions (Basic)**
- Hardcoded pairing rules
- "Wines that pair with X" endpoint
- Based on dish characteristics

### Week 7-8: AI Integration

**Priority 1: Claude API Integration**
- Pairing recommendation endpoint
- Natural language wine descriptions
- Smart pricing suggestions

**Priority 2: Vector Search (Qdrant)**
- Wine similarity search
- "Customers who liked X also liked Y"

---

## Deployment Checklist

Before deploying to production:

- [ ] Add authentication (Auth0/Clerk)
- [ ] Enable HTTPS only
- [ ] Set up proper CORS origins
- [ ] Use environment-specific configs
- [ ] Set up database backups
- [ ] Add monitoring (Sentry, Datadog)
- [ ] Rate limiting on API
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (SQLAlchemy handles this)
- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=false
- [ ] Use production-grade database (RDS)
- [ ] Set up CI/CD pipeline
- [ ] Write user documentation

---

## Useful Commands

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Access database
docker-compose exec db psql -U postgres -d sommelier_db

# Run Python shell with app context
docker-compose exec backend python -c "from app.models import *; from app.core.database import SessionLocal; db = SessionLocal()"

# Format code
docker-compose exec backend black app/

# Type checking
docker-compose exec backend mypy app/

# Run tests
docker-compose exec backend pytest

# Generate new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Rebuild after dependency changes
docker-compose up -d --build backend
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Pydantic Docs**: https://docs.pydantic.dev
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## Questions or Issues?

Check:
1. Logs first: `docker-compose logs -f`
2. API docs: http://localhost:8000/docs
3. Database state: Connect via psql
4. This guide's troubleshooting section

Happy coding! 🍷
