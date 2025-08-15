"""create users table

Revision ID: b3d70d5934a8
Revises:
Create Date: 2025-08-14 22:05:51.283629

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b3d70d5934a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    "users",
    sa.Column(
      "id",
      sa.String(36),
      primary_key=True,
      nullable=False,
      server_default=sa.text("(UUID())")
    ),
    sa.Column("name", sa.String(160), nullable=False),
    sa.Column("email", sa.String(160), nullable=False, unique=True),
    sa.Column("password_hash", sa.String(255), nullable=False),
    sa.Column(
      "role",
      sa.Enum("MASTER", "ADMIN", "USER", name="roleenum"),
      nullable=False,
      server_default=sa.text("'USER'")
    ),
    sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
    sa.Column("created_at", sa.DateTime(), nullable=False,
              server_default=sa.text("CURRENT_TIMESTAMP")),
    sa.Column("updated_at", sa.DateTime(), nullable=False,
              server_default=sa.text("CURRENT_TIMESTAMP"),
              server_onupdate=sa.text("CURRENT_TIMESTAMP")),
  )


def downgrade():
  op.drop_table("users")
