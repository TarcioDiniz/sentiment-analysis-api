import uuid
from enum import Enum

from sqlalchemy import text, Enum as SAEnum

from app.core.extensions import db


class RoleEnum(str, Enum):
  MASTER = "MASTER"
  ADMIN = "ADMIN"
  USER = "USER"


class User(db.Model):
  __tablename__ = "users"

  id = db.Column(
    db.String(36),
    primary_key=True,
    nullable=False,
    default=lambda: str(uuid.uuid4()),
  )

  name = db.Column(db.String(160), nullable=False)
  email = db.Column(db.String(160), unique=True, nullable=False, index=True)
  password_hash = db.Column(db.String(255), nullable=False)

  role = db.Column(
    SAEnum(RoleEnum, name="roleenum"),
    nullable=False,
    server_default=text("'USER'"),
    default=RoleEnum.USER,
  )

  is_active = db.Column(
    db.Boolean,
    nullable=False,
    server_default=text("1"),
    default=True,
  )

  created_at = db.Column(
    db.DateTime,
    nullable=False,
    server_default=text("CURRENT_TIMESTAMP"),
  )
  updated_at = db.Column(
    db.DateTime,
    nullable=False,
    server_default=text("CURRENT_TIMESTAMP"),
    onupdate=text("CURRENT_TIMESTAMP"),
  )
