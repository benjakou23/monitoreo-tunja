from marshmallow import Schema, fields, validate

VALID_STATUSES = ["activo", "inactivo", "mantenimiento", "falla"]

class DeviceTypeSchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(load_default=None, validate=validate.Length(max=255))

class DeviceCreateSchema(Schema):
    name           = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    ip_address     = fields.Str(load_default=None)
    mac_address    = fields.Str(load_default=None)
    serial_number  = fields.Str(load_default=None)
    brand          = fields.Str(load_default=None, validate=validate.Length(max=100))
    model          = fields.Str(load_default=None, validate=validate.Length(max=100))
    status         = fields.Str(load_default="activo", validate=validate.OneOf(VALID_STATUSES))
    device_type_id = fields.Int(load_default=None)
    location_id    = fields.Int(load_default=None)
    description    = fields.Str(load_default=None)

class DeviceUpdateSchema(Schema):
    name           = fields.Str(load_default=None, validate=validate.Length(min=2, max=150))
    ip_address     = fields.Str(load_default=None)
    mac_address    = fields.Str(load_default=None)
    serial_number  = fields.Str(load_default=None)
    brand          = fields.Str(load_default=None)
    model          = fields.Str(load_default=None)
    status         = fields.Str(load_default=None, validate=validate.OneOf(VALID_STATUSES))
    device_type_id = fields.Int(load_default=None)
    location_id    = fields.Int(load_default=None)
    description    = fields.Str(load_default=None)

