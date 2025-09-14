#!/usr/bin/env python3
"""
PostgreSQL Connection Test Script
Run this script to test your PostgreSQL database connection and setup.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test PostgreSQL database connection"""
    try:
        # Get DATABASE_URL from environment or use default Neon connection string
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_mIq6DnStlPT0@ep-raspy-flower-a1ddrzcr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
        
        print("Testing Neon PostgreSQL connection...")
        print(f"Connection URL: {DATABASE_URL[:50]}...")
        
        # Connect to PostgreSQL using connection string
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Test connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connection successful!")
        print(f"PostgreSQL Version: {version[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        print(f"\nExisting tables:")
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  No tables found. Run postgresql_schema.sql to create tables.")
        
        # Check user table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'user'
            ORDER BY ordinal_position
        """)
        user_columns = cursor.fetchall()
        
        if user_columns:
            print(f"\nUser table structure:")
            for column in user_columns:
                print(f"  - {column[0]}: {column[1]}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database setup looks good!")
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
