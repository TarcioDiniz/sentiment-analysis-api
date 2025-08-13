from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort


def require_roles(*roles):
  def decorator(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
      claims = get_jwt()
      user_roles = set(claims.get("roles", []))
      if not set(roles).issubset(user_roles):
        abort(403, message="Forbidden: missing roles")
      return fn(*args, **kwargs)

    wrapper.__name__ = fn.__name__
    return wrapper

  return decorator
