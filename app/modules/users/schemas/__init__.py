from collections import OrderedDict

from marshmallow import Schema, fields, validate, pre_load
from marshmallow_enum import EnumField

from app.modules.users.models import RoleEnum


class UserIn(Schema):
  name = fields.Str(required=True, validate=validate.Length(min=2))
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
  role = fields.Str(
    load_default=RoleEnum.USER.value,
    validate=validate.OneOf([r.value for r in RoleEnum])
  )

  @pre_load
  def normalize_role(self, data, **kwargs):
    r = data.get("role")
    if isinstance(r, str):
      data["role"] = r.upper()
    return data


class UserPatch(Schema):
  name = fields.Str(validate=validate.Length(min=2))
  password = fields.Str(load_only=True, validate=validate.Length(min=6))
  role = fields.Str(validate=validate.OneOf([r.value for r in RoleEnum]))
  is_active = fields.Bool()

  @pre_load
  def normalize_role(self, data, **kwargs):
    r = data.get("role")
    if isinstance(r, str):
      data["role"] = r.upper()
    return data


class UserOut(Schema):
  id = fields.UUID()
  name = fields.Str()
  email = fields.Email()
  role = EnumField(RoleEnum, by_value=True)
  is_active = fields.Bool()
  created_at = fields.DateTime()
  updated_at = fields.DateTime()
