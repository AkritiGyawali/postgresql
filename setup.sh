#!/bin/bash

# Quick Setup Script for Neon PostgreSQL Flask App
# This script helps you quickly set up the application

echo "🚀 Setting up Flask App with Neon PostgreSQL"
echo "============================================="

# Check if Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create and activate a virtual environment first:"
    echo "python -m venv .venv"
    echo "source .venv/bin/activate  # On Linux/Mac"
    echo ".venv\\Scripts\\activate   # On Windows"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created! Please edit it with your Gmail credentials:"
    echo "   - SECRET_KEY: Generate a strong random key"
    echo "   - User_id: Your Gmail address"
    echo "   - Pass_key: Your Gmail app password"
    echo ""
    echo "For Gmail app password setup, visit:"
    echo "https://support.google.com/accounts/answer/185833"
    echo ""
fi

# Test database connection
echo "🔗 Testing database connection..."
python test_db_connection.py

if [ $? -ne 0 ]; then
    echo "❌ Database connection failed!"
    exit 1
fi

# Initialize database
echo "🗄️  Initializing database schema..."
python init_neon_db.py

if [ $? -ne 0 ]; then
    echo "❌ Database initialization failed!"
    exit 1
fi

# Test app import
echo "🧪 Testing application..."
python -c "import app; print('✅ Application test passed!')"

if [ $? -ne 0 ]; then
    echo "❌ Application test failed!"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "===============================
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Gmail credentials"
echo "2. Run the application: python app.py"
echo "3. Visit http://localhost:8080 in your browser"
echo ""
echo "For deployment, you can use services like:"
echo "- Heroku: git push heroku main"
echo "- Railway: railway up"
echo "- Render: Connect your GitHub repo"
echo ""
