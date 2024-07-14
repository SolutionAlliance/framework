from celery import Celery

from config import Config

app = Celery()
app.config_from_object(Config)

# 注册celery 任务
from app.tasks import example 