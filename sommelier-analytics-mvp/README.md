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

**Built for**: Mid-tier restaurants ($50-100/person) that want great wine programs but can't afford a full-time sommelier.

**Market opportunity**: 70,000 US restaurants × $300/month = $252M TAM

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

**That's it!** The API is running at http://localhost:8000

---

## 📚 Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Installation & first steps | Read this first |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Complete project overview | Understand what you have |
| **[QUICKSTART.md](QUICKSTART.md)** | Test with sample data | Try it out immediately |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Developer guide | Before writing code |
| **[INDEX.md](INDEX.md)** | Documentation index | Find specific topics |

**Live API Docs**: http://localhost:8000/docs (interactive, auto-generated)

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

**Why these choices?** See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#-tech-stack)

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

**See it live**: http://localhost:8000/docs

---

## 📁 Project Structure

```
sommelier-analytics-mvp/
├── 📄 Documentation
│   ├── GETTING_STARTED.md      # Start here!
│   ├── PROJECT_SUMMARY.md      # Complete overview
│   ├── QUICKSTART.md           # 5-minute guide
│   ├── DEVELOPMENT.md          # Developer guide
│   └── INDEX.md                # Doc index
│
├── 🐳 Docker Setup
│   ├── docker-compose.yml      # Multi-container config
│   └── setup.sh                # Automated setup script
│
├── 🔧 Backend (FastAPI)
│   ├── app/
│   │   ├── main.py            # App entry point
│   │   ├── core/              # Config & database
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── api/v1/            # API endpoints
│   │       ├── restaurants.py
│   │       ├── wines.py       # Wine CRUD + CSV
│   │       ├── sales.py       # Sales CRUD + CSV
│   │       └── analytics.py   # Analytics ⭐
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container definition
│
└── 📊 Sample Data
    ├── wines_template.csv     # 8 sample wines
    └── sales_template.csv     # 10 sample sales
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

---

## 💡 Business Model

**Target Customer**: Mid-tier restaurants with serious wine programs
**Pain Point**: Can't afford $80K/year sommelier
**Solution**: $300/month software that provides 80% of the value
**ROI**: Pays for itself if it increases wine sales by just 2%

**Example**: 
- Restaurant has $200K annual wine revenue
- This tool increases sales by 10% = $20K
- Cost: $3,600/year
- **Net benefit: $16,400/year**

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#-business-value) for detailed ROI analysis.

---

## 🚀 Deployment

### Quick Deploy Options

**Railway** (Easiest):
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway up
```

**Render** (Free tier available):
- Connect GitHub repo
- Add PostgreSQL database
- Deploy!

**AWS** (Production-ready):
- ECS Fargate (Docker)
- RDS PostgreSQL
- ~$50-100/month

See deployment guides in [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 🧪 Testing

### Run Tests
```bash
docker-compose exec backend pytest
```

### Manual Testing
1. Go to http://localhost:8000/docs
2. Use interactive "Try it out" buttons
3. Upload sample CSVs from `sample-data/`

### Test Coverage
```bash
docker-compose exec backend pytest --cov=app
```

---

## 🤝 Contributing

This is a production-ready MVP. Key areas for contribution:

1. **Frontend**: Build Next.js dashboard (Week 3-4)
2. **AI Integration**: Add Claude API for pairing suggestions (Week 7-8)
3. **Mobile App**: React Native server app (Week 9-12)
4. **Integrations**: Toast, Square POS systems (Month 4+)

See [DEVELOPMENT.md](DEVELOPMENT.md#next-features-to-build) for roadmap.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change port in `docker-compose.yml` |
| Database won't start | `docker-compose restart db` |
| Migration failed | `docker-compose exec backend alembic upgrade head` |
| API returns errors | `docker-compose logs -f backend` |

Full troubleshooting guide: [DEVELOPMENT.md](DEVELOPMENT.md#common-issues--solutions)

---

## 📈 Success Metrics

After loading sample data, you should see:
- ✅ 8 wines in inventory
- ✅ 147 bottles in stock
- ✅ 10 sales transactions
- ✅ $641 revenue
- ✅ 50% average profit margin
- ✅ Top seller identified (Whispering Angel Rosé)
- ✅ Inventory alerts working

---

## 📞 Support

**Documentation**: Start with [INDEX.md](INDEX.md) to find what you need

**Issues**: 
1. Check logs: `docker-compose logs -f backend`
2. Review troubleshooting in [DEVELOPMENT.md](DEVELOPMENT.md)
3. Test API manually: http://localhost:8000/docs

**Questions**: See [GETTING_STARTED.md](GETTING_STARTED.md#getting-help)

---

## 📜 License

MIT License - See LICENSE file

---

## 🎯 Next Steps

1. ✅ Run `./setup.sh` to get started
2. ✅ Complete [GETTING_STARTED.md](GETTING_STARTED.md) tutorial
3. ✅ Upload sample data and explore analytics
4. 🚧 Build frontend dashboard (optional)
5. 🚧 Test with real restaurant data
6. 🚧 Deploy to production
7. 🚧 Start pilot with 3-5 restaurants

---

**Ready to start?** Run `./setup.sh` and visit http://localhost:8000/docs

**Questions?** Read [INDEX.md](INDEX.md) to find the right documentation.

**Building a business?** Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for market analysis and roadmap.

---

Built with ❤️ for restaurants who love wine 🍷
