# Quick Start Guide

Get your PostgreSQL database and FastAPI application running in minutes!

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ installed
- Git

## 1. Setup Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration (optional for development)
nano .env
```

## 2. Start Database

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Verify database is running
docker-compose ps
```

## 3. Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 4. Initialize Database

```bash
# Initialize database tables
python -c "from app.database import init_db; init_db()"
```

## 5. Start Application

```bash
# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 6. Access Your Application

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Optional: PgAdmin Database Management

```bash
# Start pgAdmin
docker-compose --profile tools up -d pgadmin

# Access pgAdmin at http://localhost:5050
# Login: admin@webbpulse.com / admin123
```

## Useful Commands

```bash
# Test your setup
python test-setup.py

# View database logs
docker-compose logs postgres

# Access PostgreSQL shell
docker-compose exec postgres psql -U portfolio_user -d portfolio_blog

# Stop all services
docker-compose down

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d postgres
```

## Troubleshooting

### Database Connection Issues
- Ensure Docker is running
- Check if port 5432 is available
- Verify environment variables in `.env` file

### Import Errors
- Make sure you're in the `backend` directory
- Activate your virtual environment
- Run `python test-setup.py` to verify configuration

### Port Conflicts
- Change `POSTGRES_PORT` in `.env` file
- Update `DATABASE_URL` accordingly
- Restart containers

## Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Create your first blog post
3. Set up email configuration for notifications
4. Configure production environment variables

## Production Deployment

For Railway deployment:
1. Set `DATABASE_URL` to your Railway PostgreSQL URL
2. Set `DEBUG=false`
3. Configure production `SECRET_KEY`
4. Set up `SENDGRID_API_KEY` for email notifications 