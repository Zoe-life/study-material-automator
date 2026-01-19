#!/bin/bash
# Start the Study Material Automator Web Interface

echo "Starting Study Material Automator Web Interface..."
echo "=================================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "❗ Please edit .env and add your OPENAI_API_KEY before continuing"
    echo "Press Ctrl+C to exit and configure, or Enter to continue anyway"
    read
fi

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Starting web server..."
echo "🌐 Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

cd web
python3 app.py
