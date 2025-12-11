# 🚀 Getting Started with Sommelier Analytics MVP

## What You Have

A complete, production-ready **Wine Sales Analytics Dashboard** backend with:
- ✅ Full REST API with 20+ endpoints
- ✅ PostgreSQL database with migrations
- ✅ Advanced analytics (sales trends, inventory health, profit analysis)
- ✅ CSV bulk import for wines and sales
- ✅ Docker containerization
- ✅ Auto-generated API documentation
- ✅ Sample data for testing

## Installation Methods

### Method 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh
```

That's it! The script will:
1. Check dependencies
2. Create environment file
3. Start Docker containers
4. Run database migrations
5. Verify everything is working

### Method 2: Manual Setup

```bash
# 1. Create environment file
cp backend/.env.example backend/.env

# 2. Start services
docker-compose up -d

# 3. Wait for database to be ready (10 seconds)
sleep 10

# 4. Run migrations
docker-compose exec backend alembic upgrade head

# 5. Verify it's running
curl http://localhost:8000/health
```

## First Steps After Installation

### 1. Open the API Documentation
Navigate to: http://localhost:8000/docs

You'll see the complete interactive API documentation.

### 2. Create Your First Restaurant

Click on `POST /api/v1/restaurants/` → "Try it out"

```json
{
  "name": "Your Restaurant Name",
  "email": "your@email.com",
  "city": "Atlanta",
  "state": "GA"
}
```

**Copy the `id` from the response!** You'll need it for all other requests.

### 3. Upload Sample Wine Data

Click on `POST /api/v1/wines/bulk-upload` → "Try it out"
- Enter your restaurant ID
- Upload file: `sample-data/wines_template.csv`
- Click "Execute"

You should see: `"wines_created": 8`

### 4. Upload Sample Sales Data

Click on `POST /api/v1/sales/bulk-upload` → "Try it out"
- Enter your restaurant ID
- Upload file: `sample-data/sales_template.csv`
- Click "Execute"

You should see: `"sales_created": 10`

### 5. View Your Analytics Dashboard

Click on `GET /api/v1/analytics/dashboard/{restaurant_id}` → "Try it out"
- Enter your restaurant ID
- Click "Execute"

You'll see:
```json
{
  "total_wines": 8,
  "total_bottles_in_stock": 147,
  "total_sales_last_30_days": 10,
  "revenue_last_30_days": 641.00,
  "profit_last_30_days": 320.00,
  "avg_profit_margin": 49.92,
  "top_wine_this_month": "2022 Whispering Angel Rosé",
  ...
}
```

🎉 **You're now analyzing wine sales data!**

## Explore Other Analytics

### Top & Bottom Sellers
`GET /api/v1/analytics/top-bottom-wines/{restaurant_id}`
- See which wines are selling best/worst
- View profit margins for each

### Sales Trends Over Time
`GET /api/v1/analytics/sales-trends/{restaurant_id}`
- Day-by-day sales data
- Revenue trends
- Perfect for charting

### Inventory Health Check
`GET /api/v1/analytics/inventory-health/{restaurant_id}`
- Which wines need reordering
- Which are overstocked
- Days until stockout

### Profit Analysis
`GET /api/v1/analytics/profit-analysis/{restaurant_id}`
- Profit margins by wine
- Pricing recommendations
- Year-to-date profit

## Using Your Own Data

### Prepare Your CSV Files

**Wines CSV** (wines.csv):
```csv
name,producer,vintage,varietal,region,country,wine_type,body,price,cost,inventory_count
2019 Caymus Cabernet,Caymus,2019,Cabernet Sauvignon,Napa Valley,USA,red,full,95.00,48.00,12
```

**Sales CSV** (sales.csv):
```csv
wine_name,sale_date,quantity,unit_price,unit_cost,server_name,table_number
2019 Caymus Cabernet,2025-01-08,1,95.00,48.00,John,5
```

**Important:**
- Wine names in sales.csv must **exactly match** names in wines.csv
- Dates must be in YYYY-MM-DD format
- All numeric fields must be valid numbers

### Upload Your Data

Use the bulk upload endpoints just like with sample data:
1. Upload your wines.csv to `/api/v1/wines/bulk-upload`
2. Upload your sales.csv to `/api/v1/sales/bulk-upload`
3. View analytics immediately!

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just database
docker-compose logs -f db
```

### Stop Everything
```bash
docker-compose down
```

### Restart After Changes
```bash
docker-compose restart backend
```

### Access the Database
```bash
docker-compose exec db psql -U postgres -d sommelier_db

# Useful queries:
\dt                    # List tables
SELECT COUNT(*) FROM wines;
SELECT COUNT(*) FROM sales;
SELECT * FROM restaurants;
```

### Reset Everything (⚠️ Deletes all data)
```bash
docker-compose down -v
./setup.sh
```

## What to Read Next

**If you want to...**

| Goal | Read This |
|------|-----------|
| Understand what this project does | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Learn how to use the API | [QUICKSTART.md](QUICKSTART.md) |
| Add features or modify code | [DEVELOPMENT.md](DEVELOPMENT.md) |
| Find specific documentation | [INDEX.md](INDEX.md) |

## Troubleshooting

### "Port 8000 is already in use"
Edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### "Port 5432 is already in use"
Edit `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Use port 5433 instead
```

Then update `backend/.env`:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/sommelier_db
```

### "Database connection error"
```bash
# Check database is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### "Migration failed"
```bash
# Check current migration
docker-compose exec backend alembic current

# Try running again
docker-compose exec backend alembic upgrade head

# If that fails, reset (⚠️ loses data)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## API Quick Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/restaurants/` | POST | Create restaurant |
| `/api/v1/wines/bulk-upload` | POST | Upload wines CSV |
| `/api/v1/sales/bulk-upload` | POST | Upload sales CSV |
| `/api/v1/analytics/dashboard/{id}` | GET | Dashboard summary |
| `/api/v1/analytics/top-bottom-wines/{id}` | GET | Top/bottom sellers |
| `/api/v1/analytics/sales-trends/{id}` | GET | Sales over time |
| `/api/v1/analytics/inventory-health/{id}` | GET | Stock analysis |
| `/api/v1/analytics/profit-analysis/{id}` | GET | Profit margins |

Full documentation: http://localhost:8000/docs

## Success Checklist

- [ ] Setup script ran successfully
- [ ] Can access http://localhost:8000/docs
- [ ] Created a restaurant
- [ ] Uploaded sample wines
- [ ] Uploaded sample sales
- [ ] Viewed dashboard analytics
- [ ] Explored other analytics endpoints
- [ ] Tried with your own data (optional)

## Next Steps

### Immediate (Today)
1. ✅ Complete the success checklist above
2. Explore all analytics endpoints
3. Try uploading different data scenarios

### This Week
1. Build a simple frontend to visualize the data
2. Test with real restaurant data (if available)
3. Share with potential customers for feedback

### Next 2 Weeks
1. Add authentication (see DEVELOPMENT.md)
2. Deploy to production (Railway/Render)
3. Start pilot with 3-5 restaurants

## Getting Help

1. **Check the logs**: `docker-compose logs -f backend`
2. **Test the API**: http://localhost:8000/docs
3. **Read the docs**: [INDEX.md](INDEX.md) has everything
4. **Check common issues**: [DEVELOPMENT.md](DEVELOPMENT.md)

## You're Ready!

Everything you need is running and documented. The API is production-ready, you just need to:
1. Add authentication before going live
2. Build a frontend (or integrate with existing tools)
3. Start getting customer feedback

**Your analytics dashboard is live at http://localhost:8000/docs**

Good luck! 🍷📊
