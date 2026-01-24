#!/usr/bin/env python
"""
Backend API Server - Train Induction Planning & Demand Forecasting
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn
    from app import app
    
    print("🚀 Starting KMRL AI Backend Server...")
    print("📍 API running on: http://127.0.0.1:8001")
    print("📚 API Documentation: http://127.0.0.1:8001/docs")
    print("\nEndpoints:")
    print("  - POST /api/induction/recommend - Get train deployment recommendation")
    print("  - POST /api/induction/detailed - Get detailed RL analysis")
    print("  - GET  /api/induction/status - Check RL model status")
    print("  - POST /api/demand/predict - Get demand forecast")
    print("\nPress CTRL+C to stop the server.\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8001)
