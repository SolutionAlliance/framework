from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS
from app.common.cache import RedisCache
from app.common.logger import Logger

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
log = Logger()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# swagger 配置
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['title'] = "MCD api 文档"    # 配置大标题
# swagger_config['description'] = ""   # 配置公共描述内容
# swagger_config['host'] = ""    # 请求域名
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'

# 缓存
redis = RedisCache()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 日志
    log.init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # 允许跨域请求
    CORS(app, supports_credentials=True)
    
    # 缓存
    redis.init_app(app)
    redis.connect()    

    # if app.config['SSL_REDIRECT']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    # 路由注册: 不注册app对应的服务就不会运行
    #todo 动态控制app的加载，采用反射 OR if...elif...
    api = Api(app)
    Swagger(app)
    from app.example import example_url_pattern
    example_url_pattern(api=api,app=app)
    return app
