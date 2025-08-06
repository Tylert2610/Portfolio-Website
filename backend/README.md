# Portfolio Blog API

A FastAPI backend for the portfolio website blog functionality, including content management, newsletter subscriptions, and email notifications.

## Features

- **Blog Posts**: CRUD operations for blog posts with categories
- **Newsletter Subscriptions**: Email subscription management
- **Admin Authentication**: JWT-based admin authentication
- **Email Notifications**: Newsletter confirmations and new post notifications
- **PostgreSQL Database**: Robust database with SQLAlchemy ORM
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Email**: AWS SES or SMTP
- **Documentation**: OpenAPI/Swagger

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation

1. **Clone the repository**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up PostgreSQL database**

   ```sql
   CREATE DATABASE portfolio_blog;
   CREATE USER portfolio_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE portfolio_blog TO portfolio_user;
   ```

6. **Update DATABASE_URL in .env**
   ```
   DATABASE_URL=postgresql://portfolio_user:your_password@localhost/portfolio_blog
   ```

### Running the Application

**Development mode:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Public Endpoints

- `GET /api/v1/posts` - List all published posts
- `GET /api/v1/posts/{slug}` - Get single post by slug
- `GET /api/v1/categories` - List all categories
- `POST /api/v1/subscribers/subscribe` - Subscribe to newsletter
- `POST /api/v1/subscribers/unsubscribe` - Unsubscribe from newsletter

### Admin Endpoints (Authentication Required)

- `POST /api/v1/admin/login` - Admin login
- `POST /api/v1/admin/posts` - Create new post
- `PUT /api/v1/admin/posts/{id}` - Update post
- `DELETE /api/v1/admin/posts/{id}` - Delete post
- `POST /api/v1/admin/posts/{id}/publish` - Publish post
- `POST /api/v1/admin/categories` - Create category
- `PUT /api/v1/admin/categories/{id}` - Update category
- `GET /api/v1/admin/subscribers` - List subscribers

## Database Schema

### Tables

- **users**: Admin users for content management
- **categories**: Blog post categories
- **posts**: Blog posts with content and metadata
- **subscribers**: Newsletter subscribers

### Relationships

- Posts belong to Categories (many-to-one)
- Posts belong to Users (many-to-one)
- Categories have many Posts (one-to-many)

## Email Configuration

The API supports two email methods:

### Option 1: SMTP (Gmail, etc.)

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Option 2: AWS SES

```env
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
```

## Security

- JWT tokens for admin authentication
- Password hashing with bcrypt
- CORS configuration for frontend integration
- Environment variable configuration

## Development

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/v1/endpoints/    # API endpoints
│   ├── core/                # Core utilities
│   └── utils/               # Helper utilities
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
└── README.md               # This file
```

### Adding New Endpoints

1. Create endpoint file in `app/api/v1/endpoints/`
2. Add router to `app/api/v1/api.py`
3. Update schemas if needed
4. Add tests

## Deployment

### Docker (Recommended)

1. **Build image**

   ```bash
   docker build -t portfolio-blog-api .
   ```

2. **Run container**
   ```bash
   docker run -p 8000:8000 --env-file .env portfolio-blog-api
   ```

### Manual Deployment

1. Set up PostgreSQL on your server
2. Configure environment variables
3. Install dependencies
4. Run with uvicorn or gunicorn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the Portfolio Website project.
