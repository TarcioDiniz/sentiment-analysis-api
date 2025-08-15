from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort

from app.core.responders import ok
from app.core.security import require_roles
from app.modules.users.schemas import UserIn, UserOut, UserPatch
from app.modules.users.services import create_user, update_user, delete_user, \
  get_all_users
from . import blp
from ..models import RoleEnum


@blp.route("")
class UsersList(MethodView):
  @blp.response(200, UserOut(many=True))
  @jwt_required()
  @require_roles(RoleEnum.ADMIN.value, RoleEnum.MASTER.value)
  def get(self):
    items = get_all_users()
    return ok(items)[0]

  @blp.arguments(UserIn)
  @blp.response(201, UserOut)
  @jwt_required()
  @require_roles(RoleEnum.ADMIN.value, RoleEnum.MASTER.value)
  def post(self, payload):
    try:
      u = create_user(payload)
      dto = UserOut().dump(u)
      return ok(dto, "Created", status=201)
    except ValueError as e:
      abort(400, message=str(e))


@blp.route("/users/<uuid:uid>")
class UsersItem(MethodView):
  @blp.response(200, UserOut)
  @jwt_required()
  def get(self, uid):
    from app.modules.users.repositories import get_by_id
    u = get_by_id(uid)
    if not u: abort(404, message="Not Found")
    dto = UserOut().dump(u)
    return ok(dto)

  @blp.arguments(UserPatch)
  @blp.response(200, UserOut)
  @jwt_required()
  @require_roles(RoleEnum.ADMIN.value, RoleEnum.MASTER.value)
  def patch(self, payload, uid):
    u = update_user(uid, payload)
    if not u: abort(404, message="Not Found")
    dto = UserOut().dump(u)
    return ok(dto, "Updated")

  @jwt_required()
  @require_roles(RoleEnum.ADMIN.value, RoleEnum.MASTER.value)
  def delete(self, uid):
    if not delete_user(uid): abort(404, message="Not Found")
    return ok(message="Deleted", status=204)
