# Sommelier Analytics MVP - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Docker & Docker Compose installed
- Git

### Step 1: Clone and Start

```bash
# Clone the repository (or use this directory)
cd sommelier-analytics-mvp

# Start all services (PostgreSQL + Backend API)
docker-compose up -d

# Wait for services to be healthy (~10 seconds)
docker-compose logs -f backend
```

You should see: `Application startup complete.`

### Step 2: Run Database Migrations

```bash
# Run migrations to create tables
docker-compose exec backend alembic upgrade head
```

### Step 3: Test the API

Open your browser to:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see the interactive API documentation (Swagger UI).

---

## 📊 Loading Sample Data

### Option 1: Using the API Documentation (Easiest)

1. Go to http://localhost:8000/docs
2. **Create a Restaurant**:
   - Click on `POST /api/v1/restaurants/`
   - Click "Try it out"
   - Enter:
   ```json
   {
     "name": "The Wine Cellar",
     "email": "owner@winecellar.com",
     "phone": "555-0123",
     "city": "Atlanta",
     "state": "GA"
   }
   ```
   - Click "Execute"
   - **Copy the `id` from the response** (you'll need this!)

3. **Upload Wines** (CSV):
   - Click on `POST /api/v1/wines/bulk-upload`
   - Click "Try it out"
   - Enter your restaurant ID
   - Upload `sample-data/wines_template.csv`
   - Click "Execute"

4. **Upload Sales** (CSV):
   - Click on `POST /api/v1/sales/bulk-upload`
   - Click "Try it out"
   - Enter your restaurant ID
   - Upload `sample-data/sales_template.csv`
   - Click "Execute"

### Option 2: Using cURL

```bash
# 1. Create restaurant
RESTAURANT_ID=$(curl -X POST "http://localhost:8000/api/v1/restaurants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Wine Cellar",
    "email": "owner@winecellar.com",
    "city": "Atlanta",
    "state": "GA"
  }' | jq -r '.id')

echo "Restaurant ID: $RESTAURANT_ID"

# 2. Upload wines
curl -X POST "http://localhost:8000/api/v1/wines/bulk-upload?restaurant_id=$RESTAURANT_ID" \
  -F "file=@sample-data/wines_template.csv"

# 3. Upload sales
curl -X POST "http://localhost:8000/api/v1/sales/bulk-upload?restaurant_id=$RESTAURANT_ID" \
  -F "file=@sample-data/sales_template.csv"
```

---

## 🎯 Testing the Analytics Endpoints

Once you have data loaded, try these analytics endpoints:

### 1. Dashboard Summary
```bash
# Get overall metrics
curl "http://localhost:8000/api/v1/analytics/dashboard/$RESTAURANT_ID"
```

**Returns:**
- Total wines in inventory
- Bottles in stock
- Sales & revenue (last 30 days)
- Top/slowest wines
- Inventory alerts

### 2. Top & Bottom Sellers
```bash
# Get best and worst performing wines
curl "http://localhost:8000/api/v1/analytics/top-bottom-wines/$RESTAURANT_ID?limit=5"
```

**Returns:**
- Top 5 sellers by volume
- Bottom 5 sellers (slow movers)
- Revenue and profit for each

### 3. Sales Trends
```bash
# Get daily sales trends (last 30 days)
curl "http://localhost:8000/api/v1/analytics/sales-trends/$RESTAURANT_ID"
```

**Returns:**
- Day-by-day sales data
- Total revenue per day
- Unique wines sold per day

### 4. Inventory Health
```bash
# Check which wines need reordering
curl "http://localhost:8000/api/v1/analytics/inventory-health/$RESTAURANT_ID"
```

**Returns:**
- Current inventory levels
- Days until stockout
- Reorder recommendations
- Overstocked items

### 5. Profit Analysis
```bash
# Analyze profit margins
curl "http://localhost:8000/api/v1/analytics/profit-analysis/$RESTAURANT_ID"
```

**Returns:**
- Profit per bottle
- Profit margin %
- Markup percentage
- Pricing recommendations

---

## 🧪 Testing Different Scenarios

### Add More Sales Data

Create a file `more_sales.csv`:
```csv
wine_name,sale_date,quantity,unit_price,unit_cost,server_name,table_number
2019 Opus One,2025-01-08,1,385.00,195.00,Sarah,5
2021 Cloudy Bay Sauvignon Blanc,2025-01-08,2,45.00,22.00,Mike,12
```

Upload it:
```bash
curl -X POST "http://localhost:8000/api/v1/sales/bulk-upload?restaurant_id=$RESTAURANT_ID" \
  -F "file=@more_sales.csv"
```

### Query Specific Date Ranges

```bash
# Sales trends for last week
curl "http://localhost:8000/api/v1/analytics/sales-trends/$RESTAURANT_ID?start_date=2025-01-01&end_date=2025-01-08"

# Top sellers for specific period
curl "http://localhost:8000/api/v1/analytics/top-bottom-wines/$RESTAURANT_ID?start_date=2025-01-05&end_date=2025-01-07"
```

---

## 🔍 Exploring the Data

### List All Wines
```bash
curl "http://localhost:8000/api/v1/wines/?restaurant_id=$RESTAURANT_ID&page=1&page_size=10"
```

### Search Wines
```bash
# Search by name or varietal
curl "http://localhost:8000/api/v1/wines/?restaurant_id=$RESTAURANT_ID&search=Pinot"

# Filter by type
curl "http://localhost:8000/api/v1/wines/?restaurant_id=$RESTAURANT_ID&wine_type=red"
```

### View Sales History
```bash
# All sales for the restaurant
curl "http://localhost:8000/api/v1/sales/?restaurant_id=$RESTAURANT_ID"

# Sales for a specific wine
curl "http://localhost:8000/api/v1/sales/?restaurant_id=$RESTAURANT_ID&wine_id=<WINE_ID>"

# Sales in date range
curl "http://localhost:8000/api/v1/sales/?restaurant_id=$RESTAURANT_ID&start_date=2025-01-01&end_date=2025-01-08"
```

---

## 🛠️ Development Workflow

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just database
docker-compose logs -f db
```

### Accessing the Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d sommelier_db

# Useful queries:
SELECT COUNT(*) FROM wines;
SELECT COUNT(*) FROM sales;
SELECT * FROM restaurants;
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes all data)
docker-compose down -v
```

### Restarting After Code Changes
```bash
# The backend has hot-reload enabled, but if you need to restart:
docker-compose restart backend

# Or rebuild if you changed dependencies:
docker-compose up -d --build backend
```

---

## 📈 Sample Analytics Results

After loading the sample data, you should see:

**Dashboard Summary:**
- 8 wines in inventory
- ~147 bottles in stock
- ~10 sales in last 30 days
- Revenue: ~$600
- Top wine: Whispering Angel Rosé (4 bottles sold)

**Inventory Alerts:**
- Château Margaux: Only 6 bottles (consider reorder)
- Barolo Brunate: Only 8 bottles (selling well)

**Profit Analysis:**
- Most wines have ~50-52% profit margin
- Highest markup: Whispering Angel (100%)
- Lowest margin: Opus One (49%)

---

## 🐛 Troubleshooting

### Database connection errors
```bash
# Check if PostgreSQL is running
docker-compose ps

# Check database logs
docker-compose logs db

# Recreate the database
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

### API returns 404 or errors
```bash
# Check backend logs
docker-compose logs backend

# Verify migrations ran
docker-compose exec backend alembic current

# Re-run migrations if needed
docker-compose exec backend alembic upgrade head
```

### CSV upload fails
- Ensure wine names in `sales_template.csv` exactly match wines in inventory
- Check date format is YYYY-MM-DD
- Verify all numeric fields are valid numbers

---

## 🎓 Next Steps

1. **Test with real data**: Export your POS data to CSV and upload it
2. **Build the frontend**: Create a dashboard to visualize these analytics
3. **Add authentication**: Implement user login and multi-tenant support
4. **Add AI recommendations**: Integrate Claude API for pairing suggestions
5. **Deploy to production**: Use Railway, Render, or AWS

---

## 📚 API Documentation

Full interactive documentation: **http://localhost:8000/docs**

Key endpoints:
- `POST /api/v1/restaurants/` - Create restaurant
- `POST /api/v1/wines/` - Add single wine
- `POST /api/v1/wines/bulk-upload` - Upload wines CSV
- `POST /api/v1/sales/bulk-upload` - Upload sales CSV
- `GET /api/v1/analytics/dashboard/{id}` - Dashboard summary
- `GET /api/v1/analytics/top-bottom-wines/{id}` - Best/worst sellers
- `GET /api/v1/analytics/sales-trends/{id}` - Time series data
- `GET /api/v1/analytics/inventory-health/{id}` - Reorder recommendations
- `GET /api/v1/analytics/profit-analysis/{id}` - Margin analysis

---

## 💡 Tips

- Use the interactive API docs for testing - much easier than cURL
- Start with sample data to understand the structure
- The dashboard endpoint gives you everything for a summary view
- Sales trends work best with 30+ days of data
- Inventory health calculations assume 30-day velocity

---

**You're all set!** 🎉

Head to http://localhost:8000/docs and start exploring the API.
