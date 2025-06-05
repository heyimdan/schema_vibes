#!/bin/bash

# Schema Validator Service Startup Script

echo "🚀 Starting Schema Validator Service..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if AI provider is configured
if ! grep -q "OPENAI_API_KEY=sk-" .env && ! grep -q "ANTHROPIC_API_KEY=sk-ant-" .env; then
    echo "⚠️  Warning: No AI provider API key found in .env file"
    echo "   Please add either OPENAI_API_KEY or ANTHROPIC_API_KEY to .env"
    echo "   The service will start but AI analysis will fail without a valid key."
fi

# Start the service
echo "🌟 Starting FastAPI server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop the service"

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 