#!/bin/bash
# Setup script for Sommelier Analytics MVP

set -e  # Exit on error

echo "🍷 Sommelier Analytics MVP - Full Stack Setup"
echo "=============================================="
echo ""

# Parse command line arguments
SETUP_FRONTEND=false
SKIP_BACKEND=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --with-frontend)
            SETUP_FRONTEND=true
            shift
            ;;
        --frontend-only)
            SKIP_BACKEND=true
            SETUP_FRONTEND=true
            shift
            ;;
        --backend-only)
            SETUP_FRONTEND=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./setup.sh [--with-frontend] [--frontend-only] [--backend-only]"
            exit 1
            ;;
    esac
done

# ===================
# BACKEND SETUP
# ===================

if [ "$SKIP_BACKEND" = false ]; then
    echo "🔧 Setting up Backend (FastAPI + PostgreSQL)..."
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
        echo "📝 Creating backend/.env file from template..."
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

    echo "✅ Backend setup complete!"
    echo ""
fi

# ===================
# FRONTEND SETUP
# ===================

if [ "$SETUP_FRONTEND" = true ]; then
    echo "🎨 Setting up Frontend (Next.js)..."
    echo ""

    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js 18+ first:"
        echo "   https://nodejs.org/"
        exit 1
    fi

    # Check Node version
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo "❌ Node.js version 18+ is required. You have: $(node -v)"
        echo "   Please upgrade Node.js: https://nodejs.org/"
        exit 1
    fi

    echo "✅ Node.js $(node -v) is installed"
    echo ""

    # Check if frontend directory exists
    if [ ! -d "frontend" ]; then
        echo "❌ Frontend directory not found!"
        echo "   Make sure you're running this script from the project root."
        exit 1
    fi

    cd frontend

    # Install dependencies
    echo "📦 Installing frontend dependencies..."
    if command -v npm &> /dev/null; then
        npm install
    else
        echo "❌ npm is not available. Please install Node.js with npm."
        exit 1
    fi
    echo "✅ Dependencies installed!"
    echo ""

    # Create .env.local if it doesn't exist
    if [ ! -f .env.local ]; then
        echo "📝 Creating .env.local file..."
        cp .env.local.example .env.local
        echo "✅ Created .env.local"
        echo ""
        echo "⚠️  IMPORTANT: Edit frontend/.env.local and set:"
        echo "   NEXT_PUBLIC_DEMO_RESTAURANT_ID=<your-restaurant-id>"
        echo ""
        echo "   Get your restaurant ID by:"
        echo "   1. Go to http://localhost:8000/docs"
        echo "   2. Create a restaurant (POST /api/v1/restaurants/)"
        echo "   3. Copy the 'id' from the response"
        echo ""
    else
        echo "ℹ️  .env.local already exists, skipping..."
    fi
    echo ""

    cd ..

    echo "✅ Frontend setup complete!"
    echo ""
    echo "📋 Next steps for frontend:"
    echo "   1. Initialize shadcn/ui:"
    echo "      cd frontend && npx shadcn-ui@latest init"
    echo ""
    echo "   2. Install required components:"
    echo "      npx shadcn-ui@latest add card table input label select dialog badge tabs separator skeleton"
    echo ""
    echo "   3. Set your restaurant ID in frontend/.env.local"
    echo ""
    echo "   4. Start the development server:"
    echo "      npm run dev"
    echo ""
fi

# ===================
# FINAL SUMMARY
# ===================

echo "🎉 Setup Complete!"
echo "=================="
echo ""

if [ "$SKIP_BACKEND" = false ]; then
    echo "📊 Backend (API) is running at:"
    echo "   🌐 API Documentation: http://localhost:8000/docs"
    echo "   🔍 Health Check: http://localhost:8000/health"
    echo "   📝 Alternative Docs: http://localhost:8000/redoc"
    echo ""
fi

if [ "$SETUP_FRONTEND" = true ]; then
    echo "🎨 Frontend setup ready!"
    echo "   To start: cd frontend && npm run dev"
    echo "   Will run at: http://localhost:3000"
    echo ""
fi

echo "📚 Getting Started:"
if [ "$SKIP_BACKEND" = false ]; then
    echo "   Backend:"
    echo "   1. Open http://localhost:8000/docs"
    echo "   2. Create a restaurant (POST /api/v1/restaurants/)"
    echo "   3. Upload sample data (sample-data/*.csv)"
    echo "   4. Try the analytics endpoints!"
    echo ""
fi

if [ "$SETUP_FRONTEND" = true ]; then
    echo "   Frontend:"
    echo "   1. Complete shadcn/ui setup (see instructions above)"
    echo "   2. Set restaurant ID in frontend/.env.local"
    echo "   3. Run: cd frontend && npm run dev"
    echo "   4. Open http://localhost:3000"
    echo ""
fi

echo "📖 Documentation:"
echo "   • Quick Start: cat QUICKSTART.md"
echo "   • Project Summary: cat PROJECT_SUMMARY.md"
echo "   • Development Guide: cat DEVELOPMENT.md"
if [ "$SETUP_FRONTEND" = true ]; then
    echo "   • Frontend Guide: cat frontend/README.md"
    echo "   • Frontend Setup: cat frontend/FRONTEND_SETUP.md"
fi
echo ""

echo "🛠️  Useful commands:"
if [ "$SKIP_BACKEND" = false ]; then
    echo "   Backend:"
    echo "   • View logs: docker-compose logs -f backend"
    echo "   • Stop services: docker-compose down"
    echo "   • Restart: docker-compose restart"
    echo ""
fi

if [ "$SETUP_FRONTEND" = true ]; then
    echo "   Frontend:"
    echo "   • Start dev server: cd frontend && npm run dev"
    echo "   • Build for production: cd frontend && npm run build"
    echo "   • Type check: cd frontend && npm run type-check"
    echo ""
fi

echo "💡 Pro Tips:"
echo "   • Run with --with-frontend to set up both backend and frontend"
echo "   • Run with --frontend-only to skip backend setup"
echo "   • Run with --backend-only to skip frontend setup (default)"
echo ""

echo "Happy building! 🍷📊🚀"