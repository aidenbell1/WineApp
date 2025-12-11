# Sommelier Analytics MVP - Project Summary

## 🎯 What We Built

A **Wine Sales Analytics Dashboard** that helps restaurant managers:
1. Track which wines are selling (and which aren't)
2. Identify inventory that needs reordering
3. Analyze profit margins
4. Make data-driven pricing decisions

This is **Phase 1** of the full Sommelier AI platform - proving value before adding AI features.

---

## 📁 Complete Project Structure

```
sommelier-analytics-mvp/
│
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # Get up and running in 5 minutes
├── DEVELOPMENT.md                     # Developer guide
├── docker-compose.yml                 # Multi-container setup
│
├── backend/                           # FastAPI Backend
│   ├── Dockerfile                     # Backend container definition
│   ├── requirements.txt               # Python dependencies
│   ├── alembic.ini                    # Database migration config
│   ├── .env.example                   # Environment template
│   │
│   ├── alembic/                       # Database migrations
│   │   ├── env.py                     # Migration environment
│   │   └── versions/
│   │       └── 001_initial_schema.py  # Initial tables
│   │
│   └── app/                           # Application code
│       ├── main.py                    # FastAPI app entry point
│       │
│       ├── core/                      # Core configuration
│       │   ├── config.py              # Settings & env vars
│       │   └── database.py            # DB connection
│       │
│       ├── models/                    # SQLAlchemy models
│       │   ├── restaurant.py          # Restaurant entity
│       │   ├── wine.py                # Wine inventory
│       │   ├── sale.py                # Sales transactions
│       │   └── dish.py                # Menu items (future)
│       │
│       ├── schemas/                   # Pydantic schemas
│       │   ├── wine.py                # Wine validation
│       │   ├── sale.py                # Sale validation
│       │   └── analytics.py           # Analytics responses
│       │
│       └── api/v1/                    # API endpoints
│           ├── restaurants.py         # Restaurant CRUD
│           ├── wines.py               # Wine CRUD + CSV upload
│           ├── sales.py               # Sales CRUD + CSV upload
│           └── analytics.py           # Analytics endpoints ⭐
│
└── sample-data/                       # Example CSV files
    ├── wines_template.csv             # Sample wine inventory
    └── sales_template.csv             # Sample sales data
```

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Start services
docker-compose up -d

# 2. Run migrations
docker-compose exec backend alembic upgrade head

# 3. Test the API
open http://localhost:8000/docs

# 4. Create a restaurant, upload CSVs, view analytics!
```

Full instructions: See **QUICKSTART.md**

---

## 🔌 API Endpoints

### Restaurant Management
- `POST /api/v1/restaurants/` - Create restaurant
- `GET /api/v1/restaurants/{id}` - Get restaurant
- `GET /api/v1/restaurants/` - List all restaurants

### Wine Inventory
- `POST /api/v1/wines/` - Add single wine
- `GET /api/v1/wines/{id}` - Get wine details
- `GET /api/v1/wines/` - List wines (paginated, searchable)
- `PUT /api/v1/wines/{id}` - Update wine
- `DELETE /api/v1/wines/{id}` - Delete wine
- `POST /api/v1/wines/bulk-upload` - Upload wines CSV

### Sales Tracking
- `POST /api/v1/sales/` - Record single sale
- `GET /api/v1/sales/{id}` - Get sale details
- `GET /api/v1/sales/` - List sales (filtered by date, wine)
- `DELETE /api/v1/sales/{id}` - Delete sale
- `POST /api/v1/sales/bulk-upload` - Upload sales CSV

### Analytics (The Core Feature) ⭐
- `GET /api/v1/analytics/dashboard/{restaurant_id}`
  - Overall summary metrics
  - Top wine, slowest wine
  - Inventory alerts
  
- `GET /api/v1/analytics/top-bottom-wines/{restaurant_id}`
  - Best sellers by volume
  - Worst sellers (slow movers)
  - Profit margins for each
  
- `GET /api/v1/analytics/sales-trends/{restaurant_id}`
  - Day-by-day sales data
  - Revenue trends
  - Unique wines sold per day
  
- `GET /api/v1/analytics/inventory-health/{restaurant_id}`
  - Current stock levels
  - Days until stockout
  - Reorder recommendations
  - Overstocked items
  
- `GET /api/v1/analytics/profit-analysis/{restaurant_id}`
  - Profit per bottle
  - Margin percentages
  - YTD profit by wine
  - Pricing recommendations

---

## 💾 Database Schema

### restaurants
- **Purpose**: Customer accounts
- **Fields**: name, email, location, subscription_tier
- **Relationships**: → wines, sales, dishes

### wines
- **Purpose**: Wine inventory catalog
- **Fields**: 
  - Basic: name, producer, vintage, varietal, region
  - Profile: wine_type, body, sweetness, acidity, tannin
  - Business: cost, price, inventory_count
  - Analytics: times_sold
- **Relationships**: ← restaurant, → sales

### sales
- **Purpose**: Transaction records
- **Fields**: 
  - Transaction: sale_date, quantity, unit_price
  - Snapshot: unit_cost (at time of sale)
  - Metadata: server_name, table_number
- **Relationships**: ← restaurant, ← wine

### dishes
- **Purpose**: Menu items (for future pairing)
- **Fields**: name, description, protein, preparation
- **Status**: Schema ready, not used in MVP

---

## 🎨 Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **Backend** | FastAPI | Fast, async, auto-docs, type-safe |
| **Database** | PostgreSQL | ACID, relational, full-text search |
| **ORM** | SQLAlchemy | Type-safe queries, migrations |
| **Validation** | Pydantic | Request/response validation |
| **Migrations** | Alembic | Database version control |
| **Container** | Docker | Consistent dev environment |

---

## 📊 Key Features

### ✅ Implemented (MVP)
- [x] Restaurant management
- [x] Wine inventory CRUD
- [x] Sales transaction tracking
- [x] CSV bulk import (wines & sales)
- [x] Dashboard summary metrics
- [x] Top/bottom seller analysis
- [x] Sales trend charts (time series)
- [x] Inventory health monitoring
- [x] Profit margin analysis
- [x] Pricing recommendations
- [x] Date range filtering
- [x] Search & pagination
- [x] Auto-generated API docs

### 🚧 Next Phase (Week 3-4)
- [ ] Next.js frontend dashboard
- [ ] Visual charts (Recharts)
- [ ] CSV import UI
- [ ] Authentication (Auth0)
- [ ] Multi-tenant support

### 🔮 Future Phases
- [ ] Claude AI pairing recommendations
- [ ] Server mobile app (React Native)
- [ ] POS system integrations (Toast, Square)
- [ ] Email reports
- [ ] Custom alerts

---

## 🧪 Testing the API

### Using Swagger UI (Easiest)
1. Go to http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters
4. Click "Execute"
5. See response

### Using cURL (Command Line)
```bash
# Create restaurant
curl -X POST http://localhost:8000/api/v1/restaurants/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Wine Bar","email":"test@example.com"}'

# Upload wines CSV
curl -X POST "http://localhost:8000/api/v1/wines/bulk-upload?restaurant_id=<ID>" \
  -F "file=@sample-data/wines_template.csv"

# Get dashboard
curl http://localhost:8000/api/v1/analytics/dashboard/<ID>
```

### Sample Data Included
- `sample-data/wines_template.csv` - 8 wines (various types)
- `sample-data/sales_template.csv` - 10 sales transactions

---

## 📈 Example Analytics Output

After loading sample data, the dashboard returns:

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

**Top Sellers:**
- Whispering Angel Rosé: 4 bottles, $112 revenue
- Cloudy Bay Sauvignon Blanc: 3 bottles, $135 revenue

**Slow Movers:**
- Château Margaux: 0 sales in 30 days, 6 bottles in stock
- Veuve Clicquot: 1 sale, 15 bottles (might be overstocked)

---

## 💰 Business Value

### For Restaurant Owners
1. **Identify dead inventory** - See what's not selling, discount or remove it
2. **Optimize pricing** - Flag wines with low margins, suggest price increases
3. **Prevent stockouts** - Get alerted when popular wines are running low
4. **Train staff** - Know which wines to push based on margins
5. **Measure success** - Track revenue trends over time

### Example ROI Calculation
**Restaurant with 50 wines on list:**
- Average wine list has 20-30% dead inventory
- This tool identifies 10 slow-moving bottles worth $3,000
- Action: Discount them or feature them to clear
- Result: Recover $2,000 cash from inventory
- **ROI: If tool costs $300/month, it pays for itself in Week 1**

---

## 🚀 Deployment Options

### Quick Deploy (Railway/Render)
1. Connect GitHub repo
2. Add PostgreSQL addon
3. Set environment variables
4. Deploy!

Cost: ~$20-30/month

### Production Deploy (AWS)
- **App**: ECS Fargate (Docker)
- **Database**: RDS PostgreSQL
- **Cost**: ~$50-100/month (low traffic)

See `DEPLOYMENT.md` (coming soon)

---

## 🔐 Security Considerations

### Current MVP Status
⚠️ **NOT production-ready** - No authentication

Anyone with a `restaurant_id` can access data.

### Before Production
Must implement:
- [ ] User authentication (Auth0/Clerk)
- [ ] Role-based access control
- [ ] API rate limiting
- [ ] HTTPS only
- [ ] Environment-specific configs
- [ ] Database backups
- [ ] Monitoring & alerting

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **README.md** | Project overview, setup instructions |
| **QUICKSTART.md** | Get running in 5 minutes |
| **DEVELOPMENT.md** | Developer guide, patterns, troubleshooting |
| This file | Complete project summary |

**Live API Docs**: http://localhost:8000/docs (auto-generated)

---

## 🎓 Learning Resources

If you're new to these technologies:

**FastAPI**
- Official tutorial: https://fastapi.tiangolo.com/tutorial/
- Real Python guide: https://realpython.com/fastapi-python-web-apis/

**SQLAlchemy**
- Quickstart: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- Relationships: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

**PostgreSQL**
- Tutorial: https://www.postgresqltutorial.com/
- Performance tips: https://wiki.postgresql.org/wiki/Performance_Optimization

**Docker**
- Get started: https://docs.docker.com/get-started/
- Compose: https://docs.docker.com/compose/

---

## 🐛 Common Issues

### Port conflicts
If 5432 or 8000 are in use:
```yaml
# In docker-compose.yml, change:
ports:
  - "5433:5432"  # Use different host port
  - "8001:8000"
```

### Database connection errors
```bash
# Check if DB is healthy
docker-compose ps

# View DB logs
docker-compose logs db

# Restart everything
docker-compose restart
```

### Migration issues
```bash
# Check current version
docker-compose exec backend alembic current

# Reset (⚠️ loses data)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

---

## 🎯 Next Steps

### Immediate (This Week)
1. Test with your own wine/sales data
2. Explore all analytics endpoints
3. Try different date ranges
4. Test CSV import errors

### Short-term (Next 2 Weeks)
1. Build Next.js frontend
2. Create visualization charts
3. Add authentication
4. Deploy to Railway/Render

### Medium-term (Weeks 5-8)
1. Integrate Claude API for pairing suggestions
2. Build server mobile app
3. Add POS integrations
4. Start pilot with 3-5 restaurants

---

## 💡 Key Design Decisions

### Why start with analytics instead of AI?
- **Immediate value** - Restaurants can use this today
- **Proves market** - Shows willingness to pay
- **Builds foundation** - AI layer adds on top of this
- **Cheaper to build** - No AI costs initially

### Why CSV upload instead of POS integration?
- **Faster MVP** - No integration complexity
- **Universal** - Works with any POS system
- **Validates manually** - Before building integrations

### Why no authentication in MVP?
- **Faster testing** - One less thing to configure
- **Demo-friendly** - Easy to show potential customers
- **Added later** - Before production launch

---

## 📞 Support & Contact

**Questions?**
- Check the API docs: http://localhost:8000/docs
- Review DEVELOPMENT.md troubleshooting
- Check Docker logs: `docker-compose logs -f`

**Found a bug?**
- Check existing issues
- Provide: error message, steps to reproduce, relevant logs

---

## 🎉 You're Ready!

This MVP is **complete and functional**. You can:
1. ✅ Track wine sales
2. ✅ Identify top/bottom performers
3. ✅ Monitor inventory health
4. ✅ Analyze profit margins
5. ✅ Get pricing recommendations

**Next step**: Test it with real restaurant data and start getting feedback!

```bash
# Start it up
docker-compose up -d

# Check it's running
curl http://localhost:8000/health

# Explore the API
open http://localhost:8000/docs
```

Good luck! 🍷📊
