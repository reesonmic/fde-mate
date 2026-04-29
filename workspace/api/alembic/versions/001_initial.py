"""initial - create all tables

Revision ID: 001_initial
Revises:
Create Date: 2026-04-29
"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # fde_user
    op.create_table(
        "fde_user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(200), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(256), nullable=False),
        sa.Column("avatar", sa.String(500)),
        sa.Column("roles", sa.String(200), nullable=False, server_default="fde"),
        sa.Column("level", sa.String(10), nullable=False, server_default="P5"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # task
    op.create_table(
        "task",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="todo"),
        sa.Column("priority", sa.String(10), nullable=False, server_default="p2"),
        sa.Column("assignee_id", sa.Integer, sa.ForeignKey("fde_user.id")),
        sa.Column("project_id", sa.Integer, sa.ForeignKey("project.id")),
        sa.Column("due_at", sa.DateTime),
        sa.Column("tags", sa.JSON, server_default="[]"),
        sa.Column("creator_id", sa.Integer, sa.ForeignKey("fde_user.id")),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # task_history
    op.create_table(
        "task_history",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer, sa.ForeignKey("task.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("fde_user.id"), nullable=False),
        sa.Column("op", sa.String(50), nullable=False),
        sa.Column("before", sa.JSON),
        sa.Column("after", sa.JSON),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # customer
    op.create_table(
        "customer",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("industry", sa.String(100)),
        sa.Column("scale", sa.String(20)),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("fde_user.id")),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # contact
    op.create_table(
        "contact",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("customer_id", sa.Integer, sa.ForeignKey("customer.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("title", sa.String(100)),
        sa.Column("phone", sa.String(30)),
        sa.Column("email", sa.String(200)),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # opportunity
    op.create_table(
        "opportunity",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("customer_id", sa.Integer, sa.ForeignKey("customer.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("stage", sa.String(50), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2)),
        sa.Column("close_at", sa.DateTime),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # project
    op.create_table(
        "project",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("customer_id", sa.Integer, sa.ForeignKey("customer.id")),
        sa.Column("phase", sa.String(30), nullable=False, server_default="init"),
        sa.Column("health", sa.Integer, nullable=False, server_default="100"),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("fde_user.id")),
        sa.Column("start_at", sa.DateTime, nullable=False),
        sa.Column("end_at", sa.DateTime),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # project_member
    op.create_table(
        "project_member",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.Integer, sa.ForeignKey("project.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("fde_user.id"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # milestone
    op.create_table(
        "milestone",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.Integer, sa.ForeignKey("project.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("due_at", sa.DateTime, nullable=False),
        sa.Column("done", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # risk
    op.create_table(
        "risk",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.Integer, sa.ForeignKey("project.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("level", sa.String(20), nullable=False),
        sa.Column("mitigation", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # file_meta
    op.create_table(
        "file_meta",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("ext", sa.String(20), nullable=False),
        sa.Column("size", sa.BigInteger, nullable=False),
        sa.Column("scope", sa.String(30), nullable=False),
        sa.Column("scope_id", sa.Integer),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("fde_user.id")),
        sa.Column("oss_key", sa.String(500), nullable=False),
        sa.Column("rag_indexed", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # best_practice
    op.create_table(
        "best_practice",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("scenario", sa.String(100), nullable=False),
        sa.Column("summary", sa.Text),
        sa.Column("content", sa.Text),
        sa.Column("views", sa.Integer, nullable=False, server_default="0"),
        sa.Column("rating", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # sop
    op.create_table(
        "sop",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("summary", sa.Text),
        sa.Column("content", sa.Text),
        sa.Column("downloads", sa.Integer, nullable=False, server_default="0"),
        sa.Column("rating", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # learning_path
    op.create_table(
        "learning_path",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("cover_url", sa.String(500)),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0"),
    )

    # chapter
    op.create_table(
        "chapter",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("learning_path_id", sa.Integer, sa.ForeignKey("learning_path.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("required_chapter_id", sa.Integer, sa.ForeignKey("chapter.id")),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # user_chapter_progress
    op.create_table(
        "user_chapter_progress",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("fde_user.id"), nullable=False),
        sa.Column("chapter_id", sa.Integer, sa.ForeignKey("chapter.id"), nullable=False),
        sa.Column("progress", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("completed", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # ai_session
    op.create_table(
        "ai_session",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("fde_user.id"), nullable=False),
        sa.Column("assistant_key", sa.String(50), nullable=False),
        sa.Column("mode", sa.String(20), nullable=False, server_default="smart"),
        sa.Column("title", sa.String(200)),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # ai_message
    op.create_table(
        "ai_message",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.Integer, sa.ForeignKey("ai_session.id"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("card_data", sa.String(2000)),
        sa.Column("gmt_create", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("gmt_modified", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("ai_message")
    op.drop_table("ai_session")
    op.drop_table("user_chapter_progress")
    op.drop_table("chapter")
    op.drop_table("learning_path")
    op.drop_table("sop")
    op.drop_table("best_practice")
    op.drop_table("file_meta")
    op.drop_table("risk")
    op.drop_table("milestone")
    op.drop_table("project_member")
    op.drop_table("project")
    op.drop_table("opportunity")
    op.drop_table("contact")
    op.drop_table("customer")
    op.drop_table("task_history")
    op.drop_table("task")
    op.drop_table("fde_user")
