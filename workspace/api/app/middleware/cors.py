"""
CORS Middleware Configuration
"""
# CORS is configured in main.py using FastAPI's built-in CORSMiddleware
# This file provides additional CORS utilities if needed

ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Local development
    "http://localhost:8080",  # API server
]

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

ALLOWED_HEADERS = [
    "Authorization",
    "Content-Type",
    "X-Trace-ID",
    "X-Tenant-ID",
]