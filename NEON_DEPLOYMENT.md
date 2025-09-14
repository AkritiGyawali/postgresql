# Neon PostgreSQL Deployment Guide

This guide covers deploying your Flask application with Neon PostgreSQL cloud database.

## Why Neon PostgreSQL?

- ✅ **Serverless**: Automatic scaling and hibernation
- ✅ **Cloud-native**: No infrastructure management
- ✅ **Developer-friendly**: Easy connection strings
- ✅ **Cost-effective**: Pay for what you use
- ✅ **Built-in SSL**: Secure connections by default

## Quick Deployment Steps

### 1. Local Development

```bash
# Clone/setup the project
git clone <your-repo>
cd login_auth_postgresql

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Run setup script
./setup.sh

# Or manual setup:
pip install -r requirements.txt
python init_neon_db.py
cp .env.example .env
# Edit .env with your Gmail credentials
python app.py
```

### 2. Deploy to Heroku

```bash
# Install Heroku CLI, then:
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set User_id="your-gmail@gmail.com"
heroku config:set Pass_key="your-gmail-app-password"

# The DATABASE_URL is already configured in the code
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 3. Deploy to Railway

```bash
# Install Railway CLI, then:
railway login
railway new
railway add
railway up

# Set environment variables in Railway dashboard:
# - SECRET_KEY
# - User_id  
# - Pass_key
```

### 4. Deploy to Render

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Add environment variables:
   - `SECRET_KEY`
   - `User_id`
   - `Pass_key`

### 5. Deploy to Vercel (Serverless)

```bash
# Install Vercel CLI
npm i -g vercel

# Create vercel.json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

## Environment Variables for Deployment

### Required Variables:

```bash
# Application Security
SECRET_KEY=your-very-secure-secret-key-here

# Gmail Configuration (for OTP emails)
User_id=your-gmail@gmail.com
Pass_key=your-gmail-app-password

# Database (Optional - defaults to provided Neon connection)
DATABASE_URL=postgresql://neondb_owner:npg_mIq6DnStlPT0@ep-raspy-flower-a1ddrzcr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### Gmail App Password Setup:

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → 2-Step Verification
3. At the bottom, click "App passwords"
4. Generate a new app password for "Mail"
5. Use this password as `Pass_key` in your environment variables

## Database Management

### Initialize Schema:
```bash
python init_neon_db.py
```

### Test Connection:
```bash
python test_db_connection.py
```

### Backup Data:
```bash
# Using pg_dump with Neon connection string
pg_dump "postgresql://neondb_owner:npg_mIq6DnStlPT0@ep-raspy-flower-a1ddrzcr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require" > backup.sql
```

## Monitoring and Debugging

### Application Logs:
- Check your deployment platform's logs
- Use `print()` statements for debugging (they appear in logs)

### Database Monitoring:
- Use Neon dashboard: https://neon.tech/
- Monitor connection counts and query performance

### Common Issues:

1. **Connection timeout**: Neon hibernates inactive databases
   - Solution: First request might be slow, subsequent requests are fast

2. **SSL connection errors**: 
   - Ensure connection string includes `sslmode=require`

3. **Gmail authentication errors**:
   - Use App Password, not regular password
   - Enable 2-Factor Authentication first

## Performance Optimization

### Connection Pooling:
For high-traffic applications, consider using SQLAlchemy with connection pooling:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Caching:
Add Redis caching for session data and frequently accessed data.

## Security Best Practices

1. **Environment Variables**: Never commit credentials to git
2. **HTTPS**: Always use HTTPS in production
3. **SSL Mode**: Keep `sslmode=require` in connection string
4. **Strong Secrets**: Use cryptographically strong secret keys
5. **Input Validation**: The app already includes CSRF protection

## Cost Optimization

- Neon automatically hibernates inactive databases
- Monitor usage in Neon dashboard
- Consider upgrading to paid plan for production workloads
- Use connection pooling to reduce connection overhead

## Support and Resources

- **Neon Documentation**: https://neon.tech/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

For issues with this application, check the logs and ensure all environment variables are properly set.
