# Deployment Guide

This guide provides step-by-step instructions for deploying your portfolio website with the simplest CI/CD setup.

## Overview

- **Backend + Database**: Railway (simpler than AWS, includes PostgreSQL)
- **Frontend**: Vercel (simpler than AWS S3 + CloudFront)
- **CI/CD**: GitHub Actions (automatically tests and deploys)

## Total Setup Time: ~30 minutes

## Monthly Cost: $0-5 (free tiers available)

---

## 1. Backend Deployment (Railway)

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Verify your account

### Step 2: Create Railway Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your portfolio repository
4. Railway will automatically detect it's a Python project

### Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will provision a PostgreSQL database automatically
4. Note the database connection details (available in Variables tab)

### Step 4: Configure Environment Variables

In Railway project → Variables tab, add:

```
SECRET_KEY=your-production-secret-key-generate-a-secure-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=Your Name Portfolio
DEBUG=false
LOG_SQL_QUERIES=false
```

Note: `DATABASE_URL` is automatically provided by Railway when you add PostgreSQL.

### Step 5: Deploy

1. Railway automatically deploys when you push to your connected branch
2. Your API will be available at: `https://your-app-name.railway.app`

---

## 2. Frontend Deployment (Vercel)

### Step 1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account

### Step 2: Import Project

1. Click "New Project"
2. Import your GitHub repository
3. Set Framework Preset to "Vite"
4. Set Root Directory to `frontend`

### Step 3: Configure Environment Variables

In Vercel project settings → Environment Variables:

```
VITE_API_URL=https://your-backend-name.railway.app
```

### Step 4: Deploy

1. Click "Deploy"
2. Your website will be available at: `https://your-project.vercel.app`
3. You can add a custom domain later in Vercel settings

---

## 3. CI/CD Setup (GitHub Actions)

### Step 1: Get Required Tokens

#### Railway Token:

1. Go to Railway dashboard → Account Settings → Tokens
2. Create a new token
3. Copy the token

#### Vercel Tokens:

1. Go to Vercel dashboard → Settings → Tokens
2. Create a new token
3. Copy the token
4. Also note your Vercel Org ID and Project ID from project settings

### Step 2: Add GitHub Secrets

In your GitHub repository → Settings → Secrets and Variables → Actions:

Add these secrets:

- `RAILWAY_TOKEN`: Your Railway token
- `VERCEL_TOKEN`: Your Vercel token
- `VERCEL_ORG_ID`: Your Vercel organization ID
- `VERCEL_PROJECT_ID`: Your Vercel project ID
- `VITE_API_URL`: Your Railway backend URL (https://your-backend.railway.app)

### Step 3: Test the Pipeline

1. Push any change to the main branch
2. GitHub Actions will automatically:
   - Run tests for both frontend and backend
   - Deploy backend to Railway (if tests pass)
   - Deploy frontend to Vercel (if tests pass)

---

## 4. Domain Setup (Optional)

### For Custom Domain:

1. **Vercel** (Frontend): Add custom domain in Vercel project settings
2. **Railway** (Backend): Add custom domain in Railway project settings
3. Update `VITE_API_URL` environment variable to use your custom backend domain

---

## 5. Environment Variables Reference

### Local Development (.env files):

**Backend (.env in /backend):**

```env
POSTGRES_DB=portfolio_blog
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
SECRET_KEY=dev-secret-key
SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
DEBUG=true
```

**Frontend (.env in /frontend):**

```env
VITE_API_URL=http://localhost:8000
```

### Production:

**Railway (Backend):**

- `DATABASE_URL` (auto-provided by Railway)
- `SECRET_KEY`
- `SENDGRID_API_KEY`
- `SENDGRID_FROM_EMAIL`
- `DEBUG=false`

**Vercel (Frontend):**

- `VITE_API_URL` (your Railway backend URL)

**GitHub Secrets (CI/CD):**

- `RAILWAY_TOKEN`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `VITE_API_URL`

---

## 6. Monitoring & Maintenance

### Railway Dashboard:

- Monitor backend logs and performance
- View database metrics
- Manage environment variables

### Vercel Dashboard:

- Monitor frontend deployments
- View build logs and analytics
- Manage custom domains

### GitHub Actions:

- View deployment history and logs
- Monitor test results
- Get notifications on deployment failures

---

## 7. Troubleshooting

### Common Issues:

1. **Backend deployment fails**: Check Railway logs for Python/database errors
2. **Frontend build fails**: Check if `VITE_API_URL` is set correctly in Vercel
3. **Database connection errors**: Verify `DATABASE_URL` is available in Railway
4. **CORS errors**: Ensure backend CORS settings allow your frontend domain
5. **GitHub Actions fails**: Check if all required secrets are set correctly

### Database Migrations:

Railway automatically runs migrations on deployment. If you need to run them manually:

1. Go to Railway project → your backend service
2. Open terminal
3. Run: `alembic upgrade head`

---

## Cost Breakdown

### Free Tier:

- **Railway**: 500 hours/month (≈21 days), then $5/month
- **Vercel**: Unlimited for personal projects
- **GitHub Actions**: Free for public repositories
- **Total**: $0-5/month

### Scaling:

Both platforms offer easy scaling options when your traffic grows.

---

## Alternative: AWS-based Deployment

If you prefer AWS (as mentioned in your development plan):

- **Frontend**: S3 + CloudFront (~$1-3/month)
- **Backend**: EC2 or ECS (~$5-10/month)
- **Database**: RDS (~$15-25/month)
- **Total**: ~$20-40/month

The Railway + Vercel approach is significantly simpler and more cost-effective for getting started.
