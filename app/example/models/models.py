from app.common.utils import db, rand_id
from app.common.models import TimestampMixin, SoftDeleteMixin


# 接收/发送mes消息中间表
class PB_InterfaceInvokeLog(db.Model, TimestampMixin, SoftDeleteMixin):
    """
    sFrom                         来源
    sTo                           目的地
    sType                         类型
    sKey                          关键字　：celery任务id
    sData                         参数
    tCreateTime                   上传时间
    iExecResult                   执行结果 :0-未执行　1-成功  2-失败
    sResult                       存放回写结果
    tEndTime                      接收时间
    """
    __tablename__ = "pbInterfaceInvokeLog"
    guid = db.Column(db.NVARCHAR(50), primary_key=True, unique=True, nullable=False, default=rand_id)
    sFrom = db.Column(db.NVARCHAR(200), nullable=False, default='')
    sTo = db.Column(db.NVARCHAR(200), nullable=False, default='')
    sType = db.Column(db.NVARCHAR(50), nullable=False, default='')
    sKey = db.Column(db.NVARCHAR(50), nullable=False, default='')
    sData = db.Column(db.UnicodeText, nullable=False)
    tCreateTime = db.Column(db.DateTime, nullable=False)
    iExecResult = db.Column(db.Integer, nullable=False, default=0)
    sResult = db.Column(db.UnicodeText, nullable=False, default='')
    jResult = db.Column(db.DateTime, nullable=False, default='')
    kResult = db.Column(db.DateTime, nullable=False, default='')