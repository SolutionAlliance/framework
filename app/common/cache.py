import redis
from datetime import datetime

class RedisCache(object):
    """ Redis操作函数 """

    def __init__(self):
        self.redis_session = None
        self.app = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        with self.app.app_context():
            pool = redis.ConnectionPool(host=self.app.config['REDIS_HOST'],
                                        port=self.app.config['REDIS_PORT'],
                                        db=self.app.config['REDIS_DB'],
                                        password=self.app.config['REDIS_PWD'],
                                        decode_responses=True)
            self.redis_session = redis.Redis(connection_pool=pool)

    def set(self, key, value, expired=None):
        if isinstance(value, str):
            if expired and isinstance(expired, datetime):
                dif = expired - datetime.now()
                seconds = int(dif.total_seconds())
                if seconds < 0:
                    seconds = 0
                expired = seconds
            else:
                expired = None

            self.redis_session.set(key, value, ex=expired)

    def get(self, key):
        return self.redis_session.get(key)

    def ttl(self, key):
        return self.redis_session.ttl(key)

    def expire(self, key, time):
        return self.redis_session.expire(key, time)

    def sadd(self, name, value):
        return self.redis_session.sadd(name, value)

    def smembers(self, name):
        return self.redis_session.smembers(name)

    def delete(self, name):
        self.redis_session.delete(name)