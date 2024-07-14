from marshmallow import Schema, fields

class CommonSchema(Schema):
    creator_uuid = fields.String(allow_none=True, dump_only=True)
    creator_name = fields.String(allow_none=True, dump_only=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    modify_uuid = fields.String(allow_none=True, dump_only=True)
    modify_name = fields.String(allow_none=True, dump_only=True)
    modify_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    creator_ugid = fields.String(allow_none=True, dump_only=True)