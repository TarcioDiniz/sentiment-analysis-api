from functools import wraps

from flask import abort
from flask_jwt_extended import get_jwt, jwt_required


def require_roles(*required_roles):
  def decorator(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
      claims = get_jwt()
      user_roles = claims.get("roles", []) or []
      user_roles = {str(r).upper() for r in user_roles}
      required = {str(r).upper() for r in required_roles}

      if user_roles.isdisjoint(required):
        abort(403, message="Forbidden: missing roles")

      return fn(*args, **kwargs)

    return wrapper

  return decorator
