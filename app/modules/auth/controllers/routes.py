from flask.views import MethodView
from flask_smorest import abort

from app.core.responders import ok
from app.modules.auth.schemas import LoginIn
from app.modules.auth.services import authenticate
from . import blp
from ...users.schemas import UserOut


@blp.route("/login")
class Login(MethodView):
  @blp.arguments(LoginIn)
  @blp.response(200)
  def post(self, payload):
    res = authenticate(payload["email"], payload["password"])
    if not res:
      abort(401, message="Invalid credentials")

    token, user = res
    return ok({
      "access_token": token,
      "user": UserOut().dump(user),
    })[0]
