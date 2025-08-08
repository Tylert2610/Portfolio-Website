# Railway Deployment Guide

This guide covers deploying your FastAPI backend to Railway with PostgreSQL database.

## Environment Variable Strategy

### Railway vs Local Development

**Railway (Production):**

- Railway automatically provides `DATABASE_URL` when you add a PostgreSQL service
- Use `DATABASE_URL` as the primary database configuration
- Individual PostgreSQL components are optional

**Local Development:**

- Use individual PostgreSQL components (`POSTGRES_DB`, `POSTGRES_USER`, etc.)
- `DATABASE_URL` is optional for local development

### Configuration Priority

1. **`DATABASE_URL`** (Railway) - Highest priority
2. **Individual components** (Local development) - Fallback

## Railway Setup Steps

### 1. Create Railway Project

1. Go to [Railway](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub repository
5. Select the repository

### 2. Add PostgreSQL Service

1. In your Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically:
   - Create a PostgreSQL database
   - Provide `DATABASE_URL` environment variable
   - Set up connection pooling

### 3. Configure Environment Variables

Set these environment variables in Railway dashboard:

**Required:**

```env
SECRET_KEY=your-production-secret-key-here
DEBUG=false
```

**Optional (for email functionality):**

```env
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@webbpulse.com
SENDGRID_FROM_NAME=Tyler Webb Portfolio
SENDGRID_SUBSCRIPTION_GROUP_ID=your-subscription-group-id
```

**CORS Configuration:**

```env
CORS_ORIGINS=https://webbpulse.com,https://www.webbpulse.com
```

### 4. Deploy Application

1. Railway will automatically deploy when you push to your main branch
2. Monitor deployment logs in Railway dashboard
3. Check application health at the provided URL

## Environment Variables Reference

### Railway Automatic Variables

Railway automatically provides these when you add a PostgreSQL service:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

### Manual Configuration Variables

You need to set these manually in Railway dashboard:

| Variable              | Description                 | Required | Default                   |
| --------------------- | --------------------------- | -------- | ------------------------- |
| `SECRET_KEY`          | Secret key for JWT tokens   | Yes      | -                         |
| `DEBUG`               | Debug mode                  | No       | `false`                   |
| `SENDGRID_API_KEY`    | SendGrid API key for emails | No       | -                         |
| `SENDGRID_FROM_EMAIL` | From email address          | No       | `noreply@webbpulse.com`   |
| `SENDGRID_FROM_NAME`  | From name                   | No       | `Tyler Webb Portfolio`    |
| `CORS_ORIGINS`        | Allowed CORS origins        | No       | Localhost + webbpulse.com |

## Database Migration

### Automatic Migration

The application automatically runs migrations on startup when deployed to Railway.

### Manual Migration (if needed)

```bash
# Connect to Railway CLI
railway login
railway link

# Run migrations
railway run alembic upgrade head
```

## Monitoring and Logs

### Railway Dashboard

- **Logs**: View application logs in real-time
- **Metrics**: Monitor CPU, memory, and network usage
- **Deployments**: Track deployment history and status

### Health Check

Your application includes a health check endpoint:

```
GET /health
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**

   - Verify `DATABASE_URL` is set in Railway
   - Check if PostgreSQL service is running
   - Review application logs for connection errors

2. **Migration Errors**

   - Check if migrations are compatible with Railway PostgreSQL version
   - Review migration logs in Railway dashboard

3. **Environment Variables**
   - Verify all required variables are set in Railway dashboard
   - Check variable names and values

### Debug Mode

For troubleshooting, temporarily enable debug mode:

```env
DEBUG=true
```

**Remember to disable debug mode in production!**

## Local Development

### Testing Railway Configuration

Run the Railway configuration test:

```bash
cd backend
python test_railway_config.py
```

### Simulating Railway Environment

To test with Railway-like environment locally:

```bash
# Set DATABASE_URL (simulate Railway)
export DATABASE_URL="postgresql://user:pass@host:5432/db"

# Run application
uvicorn app.main:app --reload
```

## Security Considerations

1. **Never commit sensitive data** to version control
2. **Use strong secret keys** in production
3. **Enable HTTPS** (Railway provides this automatically)
4. **Regular security updates** for dependencies
5. **Monitor application logs** for suspicious activity

## Cost Optimization

### Railway Pricing

- **Free tier**: 500 hours/month
- **Basic plan**: $5/month for additional usage
- **PostgreSQL**: Included in free tier

### Optimization Tips

1. **Use free tier efficiently**
2. **Monitor resource usage**
3. **Optimize database queries**
4. **Use connection pooling** (already configured)

## Support

- **Railway Documentation**: https://docs.railway.app
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **PostgreSQL Documentation**: https://www.postgresql.org/docs
