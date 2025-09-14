-- PostgreSQL Database Schema for Login Auth Application
-- Run this script in your PostgreSQL database to create the required tables

-- Create the user table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(15) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the showw table for stock information
CREATE TABLE IF NOT EXISTS showw (
    id SERIAL PRIMARY KEY,
    stock_name VARCHAR(100) NOT NULL,
    stock_id VARCHAR(100) NOT NULL,
    ltp DECIMAL(10, 2) NOT NULL,
    username VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES "user"(username) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
CREATE INDEX IF NOT EXISTS idx_showw_username ON showw(username);
CREATE INDEX IF NOT EXISTS idx_showw_stock_name ON showw(stock_name);

-- Insert a sample user for testing (optional)
-- Password is 'testpass123' hashed with bcrypt
-- INSERT INTO "user" (first_name, last_name, username, password, email) 
-- VALUES ('Test', 'User', 'testuser', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeGMj9n2aYKWQ7LjG', 'test@example.com');
