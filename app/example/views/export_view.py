from flask import jsonify,request
from flask_restful import Api, Resource
from sqlalchemy import func, and_, distinct, text, case
from app.example.schemas.example_schemas import Palette
from app.common.logger import logger
from app.tasks.example import hello

class ExampleView(Resource):
    def get(self, username):
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        logger.critical("Critical Hello world")
        logger.error("Fail Hello world")
        logger.warning("Warning Hello world")
        logger.info("Info Hello world")
        logger.debug(username)
        # hello.apply_async()
        # 下面就是获取 config 中的配置信息的方式
        from flask import current_app
        app = current_app._get_current_object()
        print(app.config['REDIS_HOST'])
        return {'username': username}, 200
    
    def put(self,username):
        """
        示例端点，返回两个数字的和
        ---
        tags:
          - 加法API
        
        parameters:
          - name: a
            in: query`
            type: number
            required: true
            description: 第一个数字
          - name: b
            in: query
            type: number
            required: true
            description: 第二个数字
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: 两个数字的和
            examples:
            application/json: { "result": 3,"username":username }
        """
        a = request.args.get('a', default=0, type=int)
        b = request.args.get('b', default=0, type=int)
        result = a + b
        return jsonify(result=result,username=username)
    
    def delete(self,username):
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        return {'username': username}, 200
    
    def post(self,username):
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        return {'username': username}, 200