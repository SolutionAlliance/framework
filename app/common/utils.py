import os
import decimal
import json
import datetime
import logging

from app import db
from urllib.parse import unquote
from flask_restful import reqparse
from sqlalchemy import text, func
from flask import g, request
from marshmallow import Schema, fields, ValidationError
from config import basedir

logger = logging.getLogger()


# schema校验字符串不能为空字符串
def check_details(details):
    if details == '':
        raise ValidationError('内容不能为空字符串')

def get_cursor():
    return db.engine.raw_connection()

def get_session():
    return db.create_scoped_session(options={'autocommit': True, 'autoflush': False})


def date_key(k=''):
    return k + datetime.date.today().strftime('%y%m%d') + '$'


def week_key():
    return str(int(datetime.date.today().strftime('%W')) + 1)


def year_key():
    return datetime.date.today().strftime('%Y')


# 周从1开始
def week_add_one(year_week):
    '''
    :param year_week:  str '2019-00'
    :return: str '2019-01'
    '''
    year = year_week[:-2]
    week = str(int(year_week[-2:]) + 1)
    week = week if int(week) >= 10 else ('0' + week)
    return year + week


def no_commit_session():
    return db.create_scoped_session()


def get_group():
    try:
        group_id = g.user.get('group').get('id')
        # print(group_id)
    except Exception:
        group_id = None
    return group_id


def get_user_id():
    try:
        user_id = g.user.get('id')
        # print(user_id)
    except Exception:
        user_id = None
    return user_id


def get_user_name():
    try:
        # name = g.user.get('username')
        name = g.user.get('name')
        # print(name)
    except Exception:
        name = None
    return name


def get_user_email():
    """
    获取用户邮箱
    :return:
    """
    try:
        email_address = g.user.get('email')
        print(email_address)
    except Exception as e:
        logger.error(str(e))
        email_address = ''
    return email_address


class BaseModel(object):
    creator_uuid = db.Column(db.String(50), nullable=True, default=get_user_id)
    creator_name = db.Column(db.NVARCHAR(50), nullable=True, default=get_user_name)
    create_time = db.Column(db.DateTime, nullable=True, default=lambda: datetime.datetime.now())
    modify_uuid = db.Column(db.String(50), nullable=True, default=get_user_id, onupdate=get_user_id)
    modify_name = db.Column(db.NVARCHAR(50), nullable=True, default=get_user_id, onupdate=get_user_name)
    modify_time = db.Column(db.DateTime, nullable=True, default=lambda: datetime.datetime.now(),
                            onupdate=lambda: datetime.datetime.now())
    is_delete = db.Column(db.Integer, default=0)
    group_id = db.Column(db.String(50), default=get_group)


def rand_id():
    db_session = get_session()
    res = db_session.execute('select newid() as a').first().a
    return str(res)


def permission_filter(query, model):
    try:
        ugid_list = g.user.get('datapermission').get('groups')
        query = query.filter(model.group_id.in_(ugid_list))
    except Exception as e:
        print(e)
        query = query
    return query


def remove_spaces(s):
    s = str(s)
    if not (s.startswith(' ') or s.endswith(' ') or s.startswith('\u3000') or s.endswith('\u3000')):
        return s
    s = s.strip(' ')
    s = s.strip('\u3000')
    return remove_spaces(s)


def param_check(args=(), int_type=()):
    """
    构造参数解析器
    :param args: list 解析那些request.args参数
    :param int_type: 要解析成int的有那些
    :return: dict
    """
    parse = reqparse.RequestParser(bundle_errors=True)
    for arg in args:
        if arg in int_type:
            parse.add_argument(arg, type=int, location='args', store_missing=False)
        else:
            # print(1111111)

            parse.add_argument(arg, type=str, location='args', store_missing=False)
    # print(parse)
    param = parse.parse_args()
    return param


def paginator(query, schema):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    pagination = query.paginate(page=int(page), per_page=int(per_page), error_out=False)
    total_number = pagination.total  # 获取总条数
    items = pagination.items  # 获取数据
    # print(items)
    result = schema.dump(items).data
    return {
        'data': result,
        'paging': {'page': int(page),
                   'per_page': int(per_page),
                   'total_number': int(total_number)}
    }


def super_paginator(query, schema, file_name):
    if request.args.get('excel_type') == 'excel':
        schema.context = {'file_name': file_name}
        return schema.dump(query.all()).data
    else:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        pagination = query.paginate(page=int(page), per_page=int(per_page), error_out=False)
        total_number = pagination.total  # 获取总条数
        items = pagination.items  # 获取数据
        # print(items)
        result = schema.dump(items).data
        return {
            'data': result,
            'paging': {'page': int(page),
                       'per_page': int(per_page),
                       'total_number': int(total_number)}
        }


class CommonSchema(Schema):
    creator_uuid = fields.String(allow_none=True, dump_only=True)
    creator_name = fields.String(allow_none=True, dump_only=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    modify_uuid = fields.String(allow_none=True, dump_only=True)
    modify_name = fields.String(allow_none=True, dump_only=True)
    modify_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    creator_ugid = fields.String(allow_none=True, dump_only=True)
    group_id = fields.String(allow_none=True, dump_only=True)


class TimestampMixin(object):
    creator_uuid = db.Column(db.String(50), nullable=True, default=get_user_id)
    creator_name = db.Column(db.NVARCHAR(50), nullable=True, default=get_user_name)
    create_time = db.Column(db.DateTime, nullable=True, default=lambda: datetime.datetime.now())
    modify_uuid = db.Column(db.String(50), nullable=True, default=get_user_id, onupdate=get_user_id)
    modify_name = db.Column(db.NVARCHAR(50), nullable=True, default=get_user_name, onupdate=get_user_name)
    modify_time = db.Column(db.DateTime, nullable=True, default=lambda: datetime.datetime.now(),
                            onupdate=lambda: datetime.datetime.now())
    group_id = db.Column(db.String(50), default=get_group)


def batch_update(db_session, **kwargs):
    datas = kwargs.get('datas', [])
    schema = kwargs.get('schema', None)
    model = kwargs.get('model', None)
    guid = kwargs.get('guid', None)
    parent_id = kwargs.get('parent_id', None)
    order_id = kwargs.get('order_id', None)
    is_sub = kwargs.get('is_sub', False)
    errors = []
    with db_session.begin(subtransactions=is_sub):
        for data in datas:
            op_action = data.get('op_action')
            if op_action == 'add':
                value, error = schema(exclude=(guid,)).load(data)
                if order_id:
                    value[parent_id] = order_id

                errors.extend(error)
                obj = model()
                obj.update(value)
                obj.save(db_session)
            elif op_action == 'update':
                value, error = schema().load(data)
                errors.extend(error)
                obj = db_session.query(model).filter(getattr(model, guid) == value.get(guid)).first()

                if obj:
                    obj.update(value)
                    obj.save(db_session)
            elif op_action == 'delete':
                db_session.query(model).filter(getattr(model, guid) == data.get(guid)).delete()
            else:
                errors.append('参数非法')
        if errors:
            raise TypeError(errors)


def read_config():
    config_dir = os.path.join(basedir, 'sql_config.txt')
    with open(config_dir, 'r') as f:
        try:
            config = json.loads(f.read())
            config_dict = config.get('config', {})
        except Exception as e:
            logger.exception(str(e))
            config_dict = {}

    return config_dict


def add_del_update(left_id, right_id, data):
    '''
    根据左右表的主键区分 更新/新增/删除
    :param left_id: str 区分新增的键
    :param right_id: str 区分删除的键
    :param data: list [{'left_id':'', 'right_id':''}]
    :return: update, add, delete
    '''
    update = []
    add = []
    delete = []
    for i in data:
        if not i.get(left_id):
            add.append(i)
        elif not i.get(right_id):
            delete.append(i)

        else:
            update.append(i)
    # print(update)
    return update, add, delete


def query_time(start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1)
    return start, end


def remove_exponent(num):
    num = decimal.Decimal(num)
    new_num = num.to_integral() if num == num.to_integral() else num.normalize()
    return str(new_num)



def get_sql_result(sql, **kwargs):
    db_session = kwargs.get('db_session', get_session())
    s = text(sql)
    # print('exce sql text:', s)
    result = db_session.execute(s)
    # logger.debug('get data: %s' % dataset)
    return result


def iso_year(date):
    """
    获取iso年(sql-server官方没有获取iso年的函数)
    @param date:
    @return:
    """
    # return func.extract('YEAR', date)
    return func.extract('YEAR', func.dateadd(text('week'), func.datediff(text('day'), 0, date)/7, 3))
