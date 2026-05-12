from marshmallow import Schema, fields, validate

class UserCreateSchema(Schema):
    username  = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email     = fields.Email(required=True)
    password  = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(load_default=None, validate=validate.Length(max=150))
    role_id   = fields.Int(load_default=None)
    is_active = fields.Bool(load_default=True)

class UserUpdateSchema(Schema):
    email     = fields.Email(load_default=None)
    full_name = fields.Str(load_default=None, validate=validate.Length(max=150))
    role_id   = fields.Int(load_default=None)
    is_active = fields.Bool(load_default=None)

class RoleCreateSchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    description = fields.Str(load_default=None, validate=validate.Length(max=200))

