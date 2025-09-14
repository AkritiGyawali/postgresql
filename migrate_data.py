#!/usr/bin/env python3
"""
Data Migration Script from MySQL to PostgreSQL
Usage: python migrate_data.py

This script helps migrate existing data from MySQL to PostgreSQL.
Make sure both databases are accessible and update the connection details below.
"""

import mysql.connector
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Connection (Source)
mysql_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', '')
}

# PostgreSQL Connection (Target)
postgres_config = {
    'host': os.getenv('host', 'localhost'),
    'user': os.getenv('username', 'postgres'),
    'password': os.getenv('password', ''),
    'database': os.getenv('database', '')
}

def migrate_users():
    """Migrate user data from MySQL to PostgreSQL"""
    try:
        # Connect to MySQL
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        
        # Connect to PostgreSQL
        postgres_conn = psycopg2.connect(**postgres_config)
        postgres_cursor = postgres_conn.cursor()
        
        # Fetch users from MySQL
        mysql_cursor.execute("SELECT first_name, last_name, username, password, email FROM user")
        users = mysql_cursor.fetchall()
        
        # Insert users into PostgreSQL
        for user in users:
            try:
                postgres_cursor.execute(
                    'INSERT INTO "user" (first_name, last_name, username, password, email) VALUES (%s, %s, %s, %s, %s)',
                    user
                )
                print(f"Migrated user: {user[2]}")
            except psycopg2.IntegrityError as e:
                print(f"User {user[2]} already exists or error: {e}")
                postgres_conn.rollback()
                continue
        
        postgres_conn.commit()
        print("User migration completed!")
        
        # Close connections
        mysql_cursor.close()
        mysql_conn.close()
        postgres_cursor.close()
        postgres_conn.close()
        
    except Exception as e:
        print(f"Error during user migration: {e}")

def migrate_stocks():
    """Migrate stock data from MySQL to PostgreSQL"""
    try:
        # Connect to MySQL
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        
        # Connect to PostgreSQL
        postgres_conn = psycopg2.connect(**postgres_config)
        postgres_cursor = postgres_conn.cursor()
        
        # Fetch stocks from MySQL
        mysql_cursor.execute("SELECT stock_name, stock_id, ltp, username FROM showw")
        stocks = mysql_cursor.fetchall()
        
        # Insert stocks into PostgreSQL
        for stock in stocks:
            try:
                postgres_cursor.execute(
                    "INSERT INTO showw (stock_name, stock_id, ltp, username) VALUES (%s, %s, %s, %s)",
                    stock
                )
                print(f"Migrated stock: {stock[0]} for user: {stock[3]}")
            except psycopg2.Error as e:
                print(f"Error migrating stock {stock[0]}: {e}")
                postgres_conn.rollback()
                continue
        
        postgres_conn.commit()
        print("Stock migration completed!")
        
        # Close connections
        mysql_cursor.close()
        mysql_conn.close()
        postgres_cursor.close()
        postgres_conn.close()
        
    except Exception as e:
        print(f"Error during stock migration: {e}")

if __name__ == "__main__":
    print("Starting data migration from MySQL to PostgreSQL...")
    print("Note: Update connection details in this script before running!")
    
    choice = input("Do you want to proceed with migration? (y/N): ")
    if choice.lower() == 'y':
        print("1. Migrating users...")
        migrate_users()
        
        print("2. Migrating stocks...")
        migrate_stocks()
        
        print("Migration completed!")
    else:
        print("Migration cancelled.")
