#!/bin/bash
# Setup script for Sommelier Analytics MVP

set -e  # Exit on error

echo "🍷 Sommelier Analytics MVP - Setup Script"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env (you may want to customize it later)"
else
    echo "ℹ️  backend/.env already exists, skipping..."
fi
echo ""

# Start Docker containers
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if database is ready
echo "🔍 Checking database health..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        echo "✅ Database is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Database failed to start. Check logs with: docker-compose logs db"
        exit 1
    fi
    echo "   Waiting... ($i/30)"
    sleep 1
done
echo ""

# Run database migrations
echo "🔄 Running database migrations..."
docker-compose exec -T backend alembic upgrade head
echo "✅ Database migrations complete!"
echo ""

# Check if backend is responding
echo "🔍 Checking backend health..."
for i in {1..20}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend API is ready!"
        break
    fi
    if [ $i -eq 20 ]; then
        echo "❌ Backend failed to start. Check logs with: docker-compose logs backend"
        exit 1
    fi
    echo "   Waiting... ($i/20)"
    sleep 1
done
echo ""

# Success message
echo "🎉 Setup complete!"
echo ""
echo "📊 Your Sommelier Analytics API is running at:"
echo "   🌐 API Documentation: http://localhost:8000/docs"
echo "   🔍 Health Check: http://localhost:8000/health"
echo "   📝 Alternative Docs: http://localhost:8000/redoc"
echo ""
echo "📚 Next steps:"
echo "   1. Open http://localhost:8000/docs in your browser"
echo "   2. Create a restaurant using POST /api/v1/restaurants/"
echo "   3. Upload sample data using the CSV upload endpoints"
echo "   4. Explore the analytics endpoints!"
echo ""
echo "📖 Documentation:"
echo "   • Quick Start: cat QUICKSTART.md"
echo "   • Project Summary: cat PROJECT_SUMMARY.md"
echo "   • Development Guide: cat DEVELOPMENT.md"
echo ""
echo "🛠️  Useful commands:"
echo "   • View logs: docker-compose logs -f backend"
echo "   • Stop services: docker-compose down"
echo "   • Restart: docker-compose restart"
echo ""
echo "Happy analyzing! 🍷📊"
