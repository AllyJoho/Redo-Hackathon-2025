#!/bin/bash

# BYU Major Advisor - Startup Script

echo "🎓 BYU Major Advisor - Starting Application"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  Backend:  python backend/app.py"
echo "  Frontend: cd frontend && npm start"
echo ""
echo "Or run both with: npm run dev"
echo ""
