from marshmallow import Schema, fields, validate, validates, ValidationError

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class RegisterSchema(Schema):
    username  = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email     = fields.Email(required=True)
    password  = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(load_default=None, validate=validate.Length(max=150))
    role_id   = fields.Int(load_default=None)

class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password     = fields.Str(required=True, validate=validate.Length(min=6))

