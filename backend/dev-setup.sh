#!/bin/bash

# Development Setup Script for Portfolio Blog API
# This script sets up the PostgreSQL database and starts the FastAPI application

set -e

echo "🚀 Starting Portfolio Blog API Development Environment"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created. Please review and update with your actual values."
fi

# Start PostgreSQL database
echo "🐘 Starting PostgreSQL database..."
docker-compose up -d postgres

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Check database health
if docker-compose exec postgres pg_isready -U portfolio_user -d portfolio_blog; then
    echo "✅ Database is ready!"
else
    echo "❌ Database failed to start properly. Check logs with: docker-compose logs postgres"
    exit 1
fi

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Initialize database tables
echo "🗄️  Running database migrations..."
alembic upgrade head

echo "🎉 Development environment is ready!"
echo ""
echo "📋 Next steps:"
echo "1. Start the FastAPI application: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "2. Access the API documentation: http://localhost:8000/docs"
echo "3. Access pgAdmin (optional): http://localhost:5050"
echo "4. Stop the database: docker-compose down"
echo ""
echo "🔧 Useful commands:"
echo "  - View database logs: docker-compose logs postgres"
echo "  - Access database: docker-compose exec postgres psql -U portfolio_user -d portfolio_blog"
echo "  - Stop all services: docker-compose down" 