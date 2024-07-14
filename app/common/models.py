import datetime
import random

from app.common.utils import get_user_id, get_user_name, get_group
from app import db


def str_join_space(x):
    return x + " " if x else ""


def get_session():
    # return db.create_scoped_session()
    return db.create_scoped_session(options={'autocommit': True, 'autoflush': False})


def utcnow(with_timezone=False):
    return datetime.datetime.now()


def rand_id():
    db_session = get_session()
    res = db_session.execute('select newid() as a').first().a
    # print(res)
    return str(res)


def get_random_num(digits=10):
    """
    生成一个随机数字串
    :param digits:
    :return:
    """
    return ''.join(str(random.randint(0, 9)) for _ in range(digits))


class TimestampMixin(object):
    creator_uuid = db.Column(db.String(50), nullable=True, default=get_user_id)
    creator_name = db.Column(db.NVARCHAR(50), nullable=True, default=get_user_name)
    create_time = db.Column(db.DateTime, nullable=True, default=lambda: datetime.datetime.now())
    modify_uuid = db.Column(db.String(50), nullable=True, default=get_user_id, onupdate=get_user_id)
    modify_name = db.Column(db.NVARCHAR(50), nullable=True, default=get_user_name, onupdate=get_user_name)
    modify_time = db.Column(db.DateTime, nullable=True, default=lambda: datetime.datetime.now(),
                            onupdate=lambda: datetime.datetime.now())
    group_id = db.Column(db.String(50), default=get_group)
    # tenant_id = db.Column(db.String(50), default=TENANT_ID)  # 租户id
    # creator_uuid = db.Column(db.String(50), default=CREATOR_UUID)  # 创建人id
    # creator_ugid = db.Column(db.String(50), default=CREATOR_UGID)  # 创建人组id


class SoftDeleteMixin(object):
    deleted_at = db.Column(db.DateTime)
    deleted = db.Column(db.Integer, default=0)

    def soft_delete(self, session):
        self.deleted = 1
        self.deleted_at = datetime.datetime.utcnow()
        self.save(session=session)


class LookupTableMixin(object):
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text(), nullable=True)


class IdMixin(object):
    id = db.Column(db.String(20),
                   nullable=True,
                   #                      default=generator_id,
                   primary_key=True)
