#!/usr/bin/env python3
"""
Simple script to run the Schema Validator Service with error handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work"""
    print("🔧 Testing imports...")
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def run_server():
    """Run the server"""
    print("🚀 Starting Schema Validator Service...")
    
    if not test_imports():
        return
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        print("🌐 Starting server on http://localhost:8000")
        print("📖 API docs will be available at: http://localhost:8000/docs")
        print("🔍 Health check: http://localhost:8000/api/v1/health")
        print("\n📋 Press Ctrl+C to stop the server\n")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_server() 