from flasgger import  Schema, fields
from app.common.schema import CommonSchema

class Color(Schema):
    name = fields.Str()

class Palette(Schema):
    pallete_name = fields.Str()
    colors = fields.Nested(Color, many=True)

class ExampleSchema(Schema):
    """
    ExampleSchema 标准使用方式
    """
    qa_id = fields.String()
    qa_no = fields.String(dump_only=True)
    status = fields.Integer(dump_only=True)
    customer_name = fields.String()
    style_code = fields.String()
    season_name = fields.String()
    is_qualified = fields.Integer()
    creator_name = fields.String()
    create_time = fields.DateTime(format="%Y-%m-%d")
    qa_date = fields.Date()
    storage_id = fields.String()
    storage_name = fields.String(dump_only=True)

class ExampleExtraSchema(CommonSchema):
    """
    ExampleExtraSchema 继承公共的字段
    """
    qa_id = fields.String()
    qa_no = fields.String(dump_only=True)
    status = fields.Integer(dump_only=True)
    customer_name = fields.String()
    style_code = fields.String()
    season_name = fields.String()
    is_qualified = fields.Integer()
    creator_name = fields.String()
    create_time = fields.DateTime(format="%Y-%m-%d")
    qa_date = fields.Date()
    storage_id = fields.String()
    storage_name = fields.String(dump_only=True)