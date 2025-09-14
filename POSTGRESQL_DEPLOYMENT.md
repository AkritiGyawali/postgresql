# PostgreSQL Deployment Guide

This guide will help you deploy your Flask application with PostgreSQL database.

## Local Development Setup

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from https://www.postgresql.org/download/windows/

### 2. Create Database and User

```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# Create database
CREATE DATABASE stock_tracker_db;

# Create user
CREATE USER stock_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE stock_tracker_db TO stock_user;

# Exit PostgreSQL
\q
```

### 3. Setup Tables

```bash
# Run the schema script
psql -U stock_user -d stock_tracker_db -f postgresql_schema.sql
```

### 4. Environment Configuration

Create a `.env` file:
```
host=localhost
username=stock_user
password=your_secure_password
database=stock_tracker_db
SECRET_KEY=your_very_secret_key_here
User_id=your_gmail@gmail.com
Pass_key=your_gmail_app_password
```

### 5. Install Dependencies and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Test database connection
python test_db_connection.py

# Run the application
python app.py
```

## Production Deployment

### Docker Deployment

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: stock_tracker_db
      POSTGRES_USER: stock_user
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgresql_schema.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - db
    environment:
      - host=db
      - username=stock_user
      - password=your_secure_password
      - database=stock_tracker_db
      - SECRET_KEY=your_very_secret_key_here
      - User_id=your_gmail@gmail.com
      - Pass_key=your_gmail_app_password
    volumes:
      - .:/app

volumes:
  postgres_data:
```

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
```

### Cloud Deployment (Heroku)

1. **Install Heroku CLI and create app:**
```bash
heroku create your-app-name
```

2. **Add PostgreSQL addon:**
```bash
heroku addons:create heroku-postgresql:mini
```

3. **Set environment variables:**
```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set User_id=your_gmail@gmail.com
heroku config:set Pass_key=your_gmail_app_password
```

4. **Create Procfile:**
```
web: python app.py
```

5. **Deploy:**
```bash
git add .
git commit -m "PostgreSQL migration"
git push heroku main
```

6. **Initialize database:**
```bash
heroku pg:psql < postgresql_schema.sql
```

### AWS RDS Deployment

1. **Create RDS PostgreSQL instance**
2. **Configure security groups to allow connections**
3. **Update environment variables with RDS endpoint**
4. **Deploy application to EC2/ECS/Lambda**

## Migration from MySQL

If you have existing MySQL data, use the migration script:

```bash
# Update connection details in migrate_data.py
python migrate_data.py
```

## Troubleshooting

### Common Issues:

1. **Connection refused:**
   - Ensure PostgreSQL is running
   - Check host and port configuration
   - Verify firewall settings

2. **Authentication failed:**
   - Check username and password
   - Verify user permissions

3. **Table doesn't exist:**
   - Run postgresql_schema.sql
   - Check database name

4. **Import errors:**
   - Install psycopg2-binary: `pip install psycopg2-binary`

### Logs and Debugging:

```bash
# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log

# Test connection
python test_db_connection.py

# Run app in debug mode
export FLASK_DEBUG=1
python app.py
```

## Performance Optimization

1. **Add database indexes:**
```sql
CREATE INDEX CONCURRENTLY idx_user_username ON "user"(username);
CREATE INDEX CONCURRENTLY idx_showw_username_stock ON showw(username, stock_name);
```

2. **Connection pooling:**
Consider using SQLAlchemy with connection pooling for production.

3. **Database backup:**
```bash
pg_dump -U stock_user stock_tracker_db > backup.sql
```

## Security Considerations

1. **Use environment variables for sensitive data**
2. **Enable SSL for database connections in production**
3. **Regularly update dependencies**
4. **Use strong passwords**
5. **Limit database user permissions**
