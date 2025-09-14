#!/usr/bin/env python3
"""
Neon Database Schema Initialization Script
This script creates the required tables on your Neon PostgreSQL database.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_neon_database():
    """Initialize the Neon database with required tables"""
    try:
        # Get DATABASE_URL from environment or use default Neon connection string
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_mIq6DnStlPT0@ep-raspy-flower-a1ddrzcr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
        
        print("Connecting to Neon PostgreSQL database...")
        
        # Connect to PostgreSQL using connection string
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        print("Creating tables...")
        
        # Create the user table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                username VARCHAR(15) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ User table created/verified")
        
        # Create the showw table for stock information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS showw (
                id SERIAL PRIMARY KEY,
                stock_name VARCHAR(100) NOT NULL,
                stock_id VARCHAR(100) NOT NULL,
                ltp DECIMAL(10, 2) NOT NULL,
                username VARCHAR(15) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES "user"(username) ON DELETE CASCADE
            )
        ''')
        print("✅ Stock table (showw) created/verified")
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_showw_username ON showw(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_showw_stock_name ON showw(stock_name)')
        print("✅ Indexes created/verified")
        
        # Commit the changes
        conn.commit()
        print("✅ Database schema initialization completed!")
        
        # Check existing tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"\nExisting tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Neon Database Schema Initialization")
    print("=" * 40)
    
    success = init_neon_database()
    
    if success:
        print("\n🎉 Database is ready for your application!")
        print("You can now run: python app.py")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check your connection string and try again.")
