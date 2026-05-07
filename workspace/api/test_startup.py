#!/usr/bin/env python3
"""Quick test script to start API in sandbox with SQLite."""
import asyncio
import os
import sys

# Set test environment
os.environ["APP_ENV"] = "testing"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-sandbox-testing-32chars"
os.environ["REDIS_URL"] = "memory://"

from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base

async def init_database():
    """Initialize SQLite database with tables."""
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database initialized")
    return engine

async def test_imports():
    """Test that all modules can be imported."""
    errors = []
    try:
        from app.main import app
        print("✓ Main app imported")
    except Exception as e:
        errors.append(f"Main app: {e}")
        print(f"✗ Main app import failed: {e}")

    try:
        from app.routers import auth, tasks, projects, dashboard
        print("✓ Routers imported")
    except Exception as e:
        errors.append(f"Routers: {e}")
        print(f"✗ Routers import failed: {e}")

    try:
        from app.services import task_service, auth_service
        print("✓ Services imported")
    except Exception as e:
        errors.append(f"Services: {e}")
        print(f"✗ Services import failed: {e}")

    return errors

async def main():
    """Run startup test."""
    print("=" * 60)
    print("FDE Workbench API - Sandbox Test Startup")
    print("=" * 60)

    print("\n1. Testing imports...")
    errors = await test_imports()

    if errors:
        print(f"\n✗ Import errors found: {len(errors)}")
        for e in errors:
            print(f"   - {e}")
        return 1

    print("\n2. Initializing database...")
    try:
        await init_database()
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return 1

    print("\n3. Testing basic endpoint access...")
    try:
        from app.main import app
        from httpx import ASGITransport, AsyncClient

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Test health endpoint
            response = await client.get("/api/v1/health")
            print(f"   Health check: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✓ Response: {response.json()}")
            else:
                print(f"   ✗ Unexpected status: {response.text}")
    except Exception as e:
        print(f"✗ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "=" * 60)
    print("✓ Sandbox test startup completed")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
