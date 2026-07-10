"""create tables

Revision ID: 20240901_create_tables
Revises: 
Create Date: 2024-09-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "20240901_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("name", sa.String),
        sa.Column("preferences", sa.JSON, default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sessions",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id")),
        sa.Column("subject", sa.String),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("session_id", sa.String, sa.ForeignKey("sessions.id")),
        sa.Column("role", sa.String),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("tokens_used", sa.Integer, default=0),
        sa.Column("metadata", sa.JSON, default=dict),
    )


def downgrade():
    op.drop_table("messages")
    op.drop_table("sessions")
    op.drop_table("users")