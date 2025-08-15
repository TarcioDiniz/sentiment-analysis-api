from marshmallow import Schema, fields

class LoginIn(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
