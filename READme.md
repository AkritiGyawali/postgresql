# Stock tracker web app #

__The web app helps tracking stock price__

This consists of the code for signin and signup (authentication page). If you are a beginner learning to build a webapp that incorporates user login and register (user authentication) along with the PostgreSQL database, this repo is for you.

## Database Migration from MySQL to PostgreSQL

This application has been migrated from MySQL to PostgreSQL. Follow these steps to set up the database:

### Prerequisites
- Python virtual environment activated
- Internet connection (for Neon cloud database)

### Database Setup (Neon PostgreSQL Cloud)

This application is configured to use **Neon PostgreSQL** cloud database for easy deployment.

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database Schema:**
   ```bash
   python init_neon_db.py
   ```

3. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and update:
   ```bash
   cp .env.example .env
   # Edit .env with your Gmail credentials for OTP functionality
   ```

4. **Test Database Connection:**
   ```bash
   python test_db_connection.py
   ```

### Environment Variables

The application uses these environment variables (see `.env.example`):

- `DATABASE_URL`: Neon PostgreSQL connection string (already configured)
- `SECRET_KEY`: Flask secret key for session security  
- `User_id`: Your Gmail address for OTP emails
- `Pass_key`: Your Gmail app password

### For Different Database (Optional)

If you want to use a different PostgreSQL database, update the `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=postgresql://username:password@host:port/database
```

### Changes Made During Migration

- Replaced `mysql.connector` with `psycopg2-binary`
- Updated SQL queries to use PostgreSQL syntax (quoted table names)
- Removed MySQL-specific code
- Updated requirements.txt with PostgreSQL dependencies

### Running the Application

```bash
python app.py
```

The application will run on `http://0.0.0.0:8080`