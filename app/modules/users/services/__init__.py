import uuid

from passlib.hash import bcrypt

from app.core.extensions import db
from app.modules.users.models import User, RoleEnum
from app.modules.users.repositories import get_by_id, get_by_email, add, remove, \
  paginate as repo_paginate, get_all
from app.modules.users.schemas import UserOut


def create_user(data: dict) -> User:
  if get_by_email(data["email"]):
    raise ValueError("Email already in use")
  u = User(
    name=data["name"],
    email=data["email"],
    password_hash=bcrypt.hash(data["password"]),
    role=RoleEnum(data["role"])
  )
  return add(u)


def update_user(uid: uuid, data: dict) -> User | None:
  u = get_by_id(uid)
  if not u: return None
  if "name" in data: u.name = data["name"]
  if "password" in data: u.password_hash = bcrypt.hash(data["password"])
  if "role" in data: u.role = RoleEnum(data["role"])
  if "is_active" in data: u.is_active = bool(data["is_active"])
  db.session.commit()
  return u


def delete_user(uid: uuid) -> bool:
  u = get_by_id(uid)
  if not u: return False
  remove(u)
  return True


def list_users(page: int, take: int, search: str | None):
  return repo_paginate(page, take, search)


def get_all_users():
  return UserOut(many=True).dump(get_all())
