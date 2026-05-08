#!/usr/bin/env python3
"""
Seed test data for FDE Mate platform.
Creates: 5 users, 10 tasks, 3 projects, 5 customers, 8 files
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.user import User
from app.models.task import Task, TaskHistory
from app.models.project import Project, ProjectMember, Risk
from app.models.customer import Customer, Contact, Opportunity
from app.models.file import File


# Test data
USERS = [
    {"name": "admin", "email": "admin@fde.local", "password": "admin123", "roles": "admin,fde", "level": "P8"},
    {"name": "吾明", "email": "wuming@test.com", "password": "test123", "roles": "fde", "level": "P6"},
    {"name": "张伟", "email": "zhangwei@test.com", "password": "test123", "roles": "fde", "level": "P5"},
    {"name": "李娜", "email": "lina@test.com", "password": "test123", "roles": "fde", "level": "P7"},
    {"name": "王强", "email": "wangqiang@test.com", "password": "test123", "roles": "admin", "level": "P8"},
]

PROJECTS = [
    {"name": "阿里云电商改造", "description": "大型电商平台微服务改造", "phase": "delivery", "owner_id": 2, "health": "yellow"},
    {"name": "智能客服系统", "description": "AI驱动的客服系统建设", "phase": "uat", "owner_id": 3, "health": "green"},
    {"name": "数据中台项目", "description": "企业级数据中台建设", "phase": "requirements", "owner_id": 2, "health": "red"},
]

TASKS = [
    {"title": "完成客户初步沟通", "description": "与阿里巴巴技术团队进行需求对接", "status": "done", "priority": "p0", "assignee_id": 2, "project_id": 1, "creator_id": 2, "tags": ["客户沟通", "需求"]},
    {"title": "编写技术方案文档", "description": "输出微服务架构改造方案", "status": "in_progress", "priority": "p0", "assignee_id": 2, "project_id": 1, "creator_id": 1, "tags": ["文档", "架构"]},
    {"title": "数据库迁移评估", "description": "评估MySQL到PolarDB的迁移成本", "status": "todo", "priority": "p1", "assignee_id": 3, "project_id": 1, "creator_id": 2, "tags": ["数据库"]},
    {"title": "API接口设计", "description": "设计Restful API规范", "status": "review", "priority": "p1", "assignee_id": 2, "project_id": 2, "creator_id": 3, "tags": ["API", "设计"]},
    {"title": "AI模型选型", "description": "评估NLP模型方案", "status": "todo", "priority": "p2", "assignee_id": 4, "project_id": 2, "creator_id": 2, "tags": ["AI"]},
    {"title": "周报提交", "description": "本周工作汇报", "status": "todo", "priority": "p0", "assignee_id": 2, "project_id": None, "creator_id": 1, "tags": ["周报"]},
    {"title": "客户需求评审", "description": "评审新功能需求", "status": "done", "priority": "p1", "assignee_id": 3, "project_id": 3, "creator_id": 1, "tags": ["评审"]},
    {"title": "技术分享准备", "description": "准备季度技术分享", "status": "blocked", "priority": "p2", "assignee_id": 4, "project_id": None, "creator_id": 1, "tags": ["分享"]},
    {"title": "代码Review", "description": "Review团队成员代码", "status": "in_progress", "priority": "p1", "assignee_id": 2, "project_id": 1, "creator_id": 1, "tags": ["CodeReview"]},
    {"title": "客户培训", "description": "客户操作培训", "status": "todo", "priority": "p0", "assignee_id": 2, "project_id": 2, "creator_id": 3, "tags": ["培训"]},
]

CUSTOMERS = [
    {"name": "阿里巴巴集团", "industry": "电商", "scale": "超大型", "owner_id": 2},
    {"name": "腾讯科技", "industry": "互联网", "scale": "超大型", "owner_id": 3},
    {"name": "字节跳动", "industry": "互联网", "scale": "大型", "owner_id": 2},
    {"name": "华为云", "industry": "云计算", "scale": "大型", "owner_id": 4},
    {"name": "美团", "industry": "本地生活", "scale": "超大型", "owner_id": 3},
]

FILES = [
    {"name": "项目启动文档.pdf", "type": "文档", "size": 2048576, "uploader_id": 2, "path": "/projects/1/docs/"},
    {"name": "架构设计图.vsdx", "type": "图表", "size": 1024768, "uploader_id": 2, "path": "/projects/1/design/"},
    {"name": "会议纪要-0301.docx", "type": "文档", "size": 512000, "uploader_id": 3, "path": "/meeting/2026/"},
    {"name": "API接口规范.yaml", "type": "代码", "size": 102400, "uploader_id": 4, "path": "/projects/2/api/"},
    {"name": "测试报告.xlsx", "type": "表格", "size": 768000, "uploader_id": 2, "path": "/qa/reports/"},
    {"name": "部署脚本.sh", "type": "代码", "size": 15360, "uploader_id": 3, "path": "/devops/scripts/"},
    {"name": "用户手册.pdf", "type": "文档", "size": 4096000, "uploader_id": 2, "path": "/docs/manuals/"},
    {"name": "数据库设计.sql", "type": "代码", "size": 256000, "uploader_id": 4, "path": "/projects/1/db/"},
]


async def seed_data():
    database_url = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://root:20260227@172.17.0.2:3306/fde_workbench"
    )

    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("🌱 Starting seed data insertion...")

        # 1. Create users
        print("\n👥 Creating users...")
        user_map = {}
        for user_data in USERS:
            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            if result.scalar_one_or_none():
                print(f"  User exists: {user_data['email']}")
                continue

            password_hash = bcrypt.hashpw(
                user_data["password"].encode(),
                bcrypt.gensalt()
            ).decode()

            new_user = User(
                name=user_data["name"],
                email=user_data["email"],
                password_hash=password_hash,
                roles=user_data["roles"],
                level=user_data["level"],
                avatar="",
            )
            session.add(new_user)
            await session.flush()
            user_map[user_data["email"]] = new_user.id
            print(f"  ✓ Created: {user_data['name']} ({user_data['email']})")

        await session.commit()

        # Get all user IDs
        result = await session.execute(select(User.id))
        all_user_ids = [r[0] for r in result.all()]
        if not all_user_ids:
            print("❌ No users found!")
            return

        # 2. Create projects
        print("\n📁 Creating projects...")
        for proj_data in PROJECTS:
            result = await session.execute(
                select(Project).where(Project.name == proj_data["name"])
            )
            if result.scalar_one_or_none():
                print(f"  Project exists: {proj_data['name']}")
                continue

            new_proj = Project(
                name=proj_data["name"],
                description=proj_data["description"],
                phase=proj_data["phase"],
                owner_id=proj_data["owner_id"],
                health=proj_data["health"],
                budget=Decimal("1000000.00"),
                budget_spent=Decimal("250000.00"),
                progress=35 if proj_data["phase"] == "delivery" else 60 if proj_data["phase"] == "uat" else 15,
                start_at=datetime.now() - timedelta(days=90),
                end_at=datetime.now() + timedelta(days=180),
                next_milestone="需求评审完成",
                milestone_date=datetime.now() + timedelta(days=7),
                risk_count=2 if proj_data["health"] == "red" else 1 if proj_data["health"] == "yellow" else 0,
            )
            session.add(new_proj)
            await session.flush()
            print(f"  ✓ Created: {proj_data['name']}")

        await session.commit()

        # 3. Create tasks
        print("\n📝 Creating tasks...")
        tasks_created = 0
        for task_data in TASKS:
            result = await session.execute(
                select(Task).where(Task.title == task_data["title"])
            )
            if result.scalar_one_or_none():
                continue

            due_at = datetime.now() + timedelta(days=3) if task_data["priority"] == "p0" else \
                     datetime.now() + timedelta(days=7) if task_data["priority"] == "p1" else \
                     datetime.now() + timedelta(days=14)

            new_task = Task(
                title=task_data["title"],
                description=task_data["description"],
                status=task_data["status"],
                priority=task_data["priority"],
                assignee_id=task_data["assignee_id"],
                project_id=task_data["project_id"],
                creator_id=task_data["creator_id"],
                tags=task_data["tags"],
                due_at=due_at,
            )
            session.add(new_task)
            tasks_created += 1

        await session.commit()
        print(f"  ✓ Created {tasks_created} tasks")

        # 4. Create customers
        print("\n🏢 Creating customers...")
        for cust_data in CUSTOMERS:
            result = await session.execute(
                select(Customer).where(Customer.name == cust_data["name"])
            )
            if result.scalar_one_or_none():
                print(f"  Customer exists: {cust_data['name']}")
                continue

            new_cust = Customer(
                name=cust_data["name"],
                industry=cust_data["industry"],
                scale=cust_data["scale"],
                owner_id=cust_data["owner_id"],
                contacts=[],
                opportunities=[],
            )
            session.add(new_cust)
            await session.flush()
            print(f"  ✓ Created: {cust_data['name']}")

        await session.commit()

        # 5. Create files
        print("\n📄 Creating files...")
        for file_data in FILES:
            result = await session.execute(
                select(File).where(File.name == file_data["name"])
            )
            if result.scalar_one_or_none():
                continue

            new_file = File(
                name=file_data["name"],
                type=file_data["type"],
                size=file_data["size"],
                uploader_id=file_data["uploader_id"],
                path=file_data["path"],
                url=f"/files{file_data['path']}{file_data['name']}",
            )
            session.add(new_file)

        await session.commit()
        print(f"  ✓ Created {len(FILES)} files")

        print("\n✅ Seed data insertion completed!")
        print(f"\n📊 Summary:")
        print(f"  - Users: {len(USERS)}")
        print(f"  - Projects: {len(PROJECTS)}")
        print(f"  - Tasks: {len(TASKS)}")
        print(f"  - Customers: {len(CUSTOMERS)}")
        print(f"  - Files: {len(FILES)}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())
