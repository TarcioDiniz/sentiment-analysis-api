from datetime import timedelta

from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from app.modules.users.repositories import get_by_email


def authenticate(email: str, password: str):
  u = get_by_email(email)
  if not u or not u.is_active:
    return None
  if not bcrypt.verify(password, u.password_hash):
    return None

  claims = {"roles": [u.role.value], "uid": u.id, "email": u.email}
  token = create_access_token(
    identity=str(u.id),
    additional_claims=claims,
    expires_delta=timedelta(hours=8),
  )
  return token, u
