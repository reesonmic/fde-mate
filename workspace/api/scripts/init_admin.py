"""
Initialize admin user script.
Run this after database migrations to create default admin user.
"""
import asyncio
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.user import User


ADMIN_USER = {
    "name": "admin",
    "email": "admin@fde.local",
    "password": "admin123",
    "roles": "admin,fde",
    "level": "P8",
}


async def init_admin():
    # Get database URL from environment or use default
    database_url = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://root:20260227@172.17.0.2:3306/fde_workbench"
    )

    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if admin user exists
        result = await session.execute(
            select(User).where(User.email == ADMIN_USER["email"])
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"Admin user already exists: {existing_user.email} (id={existing_user.id})")
            return

        # Hash password
        password_hash = bcrypt.hashpw(
            ADMIN_USER["password"].encode(),
            bcrypt.gensalt()
        ).decode()

        # Create admin user
        new_user = User(
            name=ADMIN_USER["name"],
            email=ADMIN_USER["email"],
            password_hash=password_hash,
            roles=ADMIN_USER["roles"],
            level=ADMIN_USER["level"],
            avatar="",
        )

        session.add(new_user)
        await session.commit()

        print(f"Admin user created successfully!")
        print(f"  Email: {ADMIN_USER['email']}")
        print(f"  Password: {ADMIN_USER['password']}")
        print(f"  Roles: {ADMIN_USER['roles']}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_admin())
