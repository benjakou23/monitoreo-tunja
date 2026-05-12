from marshmallow import Schema, fields, validate

VALID_STATUSES = ["activa", "reconocida", "resuelta"]

class AlertSeveritySchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    level       = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    color       = fields.Str(load_default=None, validate=validate.Length(max=20))
    description = fields.Str(load_default=None, validate=validate.Length(max=255))

class AlertCreateSchema(Schema):
    title       = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    message     = fields.Str(required=True, validate=validate.Length(min=5))
    device_id   = fields.Int(load_default=None)
    metric_id   = fields.Int(load_default=None)
    severity_id = fields.Int(required=True)
    status      = fields.Str(load_default="activa", validate=validate.OneOf(VALID_STATUSES))

class AlertUpdateSchema(Schema):
    title       = fields.Str(load_default=None, validate=validate.Length(min=3, max=200))
    message     = fields.Str(load_default=None)
    severity_id = fields.Int(load_default=None)
    status      = fields.Str(load_default=None, validate=validate.OneOf(VALID_STATUSES))

class AlertAcknowledgeSchema(Schema):
    user_id = fields.Int(required=True)

class AlertResolveSchema(Schema):
    user_id  = fields.Int(required=True)
    message  = fields.Str(load_default=None)

