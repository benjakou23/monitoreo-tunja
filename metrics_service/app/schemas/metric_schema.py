from marshmallow import Schema, fields, validate

VALID_STATUSES = ["normal", "warning", "critical"]

class MetricTypeCreateSchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    unit        = fields.Str(load_default=None, validate=validate.Length(max=30))
    description = fields.Str(load_default=None, validate=validate.Length(max=255))
    min_value   = fields.Float(load_default=None)
    max_value   = fields.Float(load_default=None)

class MetricCreateSchema(Schema):
    device_id      = fields.Int(required=True)
    metric_type_id = fields.Int(required=True)
    value          = fields.Float(required=True)
    unit           = fields.Str(load_default=None, validate=validate.Length(max=30))
    status         = fields.Str(load_default="normal", validate=validate.OneOf(VALID_STATUSES))
    recorded_at    = fields.DateTime(load_default=None)

class MetricBulkCreateSchema(Schema):
    metrics = fields.List(fields.Nested(MetricCreateSchema), required=True)

