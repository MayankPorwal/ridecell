from marshmallow import Schema, fields


class ParkingSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    status = fields.Str(required=True)
    cost = fields.Float()



