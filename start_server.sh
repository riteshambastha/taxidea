#!/bin/bash

# TaxIdea Web Platform Startup Script

echo "============================================"
echo "TaxIdea - Property Tax Appeal Platform"
echo "============================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip3 install Flask
    echo ""
fi

# Navigate to project directory
cd "$(dirname "$0")"

# Start the server
echo "🚀 Starting web server..."
echo ""
echo "✅ Platform is running at:"
echo "   🌐 http://localhost:5001"
echo ""
echo "📱 Open your browser and navigate to the URL above"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo ""

python3 app.py

