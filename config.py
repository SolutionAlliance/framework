from datetime import timedelta
import os
from urllib import parse
from celery.schedules import crontab
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 邮件
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mcd.com.cn')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SUBJECT_PREFIX = '[FLASK]'
    FLASK_MAIL_SENDER = 'FLASK Admin <FLASK@example.com>'
    
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    FLASK_POSTS_PER_PAGE = 20
    FLASK_FOLLOWERS_PER_PAGE = 50
    FLASK_COMMENTS_PER_PAGE = 30
    FLASK_SLOW_DB_QUERY_TIME = 0.5
    # redis 
    REDIS_HOST = os.getenv('REDIS_HOST') or '127.0.0.1'
    REDIS_PORT = int(os.getenv('REDIS_PORT',0)) or 6379
    REDIS_DB = os.getenv('REDIS_DB') or '0'
    REDIS_PWD = os.getenv('REDIS_PWD') or ''
    # _redis_url = "redis://:{pwd}@{host}:{port}/".format(pwd=REDIS_PWD, host=REDIS_HOST, port=REDIS_PORT)
    _redis_url = "redis://{host}:{port}/".format(host=REDIS_HOST, port=REDIS_PORT)
    
    # mysql
    if os.environ.get('USE_MYSQL'):
        DATABASE_USER  = os.getenv('DATABASE_USER') or 'root'
        DATABASE_PASS  = os.getenv('DATABASE_PASS') or 'root'
        DATABASE_HOST  = os.getenv('DATABASE_HOST') or '127.0.0.1'
        DATABASE_DB  =parse.quote_plus(os.getenv('DATABASE_DB') or "") 
        DATABASE_PORT  = os.getenv('DATABASE_PORT') or 3306
        SQLALCHEMY_DATABASE_URI  = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

    # loguru
    # log 输入路径
    LOG_PATH =os.getenv("LOG_PATH") or basedir+'/logs/'
    # log 文件名称
    LOG_NAME = os.getenv("LOG_NAME") or "run.log"
    # log 格式
    LOG_FORMAT = os.getenv("LOG_FORMAT") or ""
    # log 翻转时间
    LOG_ROTATION = os.getenv("LOG_ROTATION") or  60 * 60
    # 是否异步
    LOG_ENQUEUE = os.getenv("LOG_ENQUEUE") or True
    # 是否序列化
    LOG_SERIALIZE = os.getenv("LOG_SERIALIZE") or True

    # celery config
    # https://celery.xgqyq.com/%E9%85%8D%E7%BD%AE%E5%92%8C%E9%BB%98%E8%AE%A4%E9%85%8D%E7%BD%AE.html#%E7%A4%BA%E4%BE%8B%E9%85%8D%E7%BD%AE
    BROKER_URL = _redis_url+"2"
    CELERY_RESULT_BACKEND = _redis_url+"3"
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERY_TIMEZONE = 'Asia/Shanghai'
    # 定时任务
    CELERYBEAT_SCHEDULE = {
        # 案例定时任务
        'every-year': {
            'task': 'app.tasks.example.hello',
            'schedule': timedelta(seconds=50)
        }
    }
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    if not os.environ.get('USE_MYSQL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')  or \
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    if not os.environ.get('USE_MYSQL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    if os.environ.get('USE_MYSQL') or True:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 通过电子邮件将错误发送给admin
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASK_MAIL_SENDER,
            toaddrs=[cls.FLASK_ADMIN],
            subject=cls.FLASK_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
