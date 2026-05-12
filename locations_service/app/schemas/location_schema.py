from marshmallow import Schema, fields, validate

class LocationCreateSchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    building    = fields.Str(load_default=None, validate=validate.Length(max=100))
    floor       = fields.Str(load_default=None, validate=validate.Length(max=50))
    room        = fields.Str(load_default=None, validate=validate.Length(max=100))
    description = fields.Str(load_default=None)
    is_active   = fields.Bool(load_default=True)

class LocationUpdateSchema(Schema):
    name        = fields.Str(load_default=None, validate=validate.Length(min=2, max=150))
    building    = fields.Str(load_default=None, validate=validate.Length(max=100))
    floor       = fields.Str(load_default=None, validate=validate.Length(max=50))
    room        = fields.Str(load_default=None, validate=validate.Length(max=100))
    description = fields.Str(load_default=None)
    is_active   = fields.Bool(load_default=None)

