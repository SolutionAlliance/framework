import time
import datetime
import os
import zipfile
from loguru import logger

class Logger(object):
    def __init__(self, app=None):
        pass

    def init_app(self,app):
        self.app = app
        path = self.app.config['LOG_NAME']
        if self.app.config['LOG_PATH'] is not None:
            path = os.path.join(self.app.config['LOG_PATH'], self.app.config['LOG_NAME'])

        def should_rotate(message, file):
            filepath = os.path.abspath(file.name)
            creation = os.path.getctime(filepath)
            now = message.record["time"].timestamp()
            return now - creation > self.app.config['LOG_ROTATION']

        def should_retention(logs):
            """ 
            检查是否需要进行压缩
            """
            # 依次查找写入
            file_list = list()
            for log in logs:
                file_path = os.path.abspath(log)

                if file_path.endswith(".zip"):
                    continue

                if time.gmtime(time.time() - os.path.getctime(file_path)).tm_mday == 7:
                    file_list.append(file_path)

            if file_list:
                self.zip_logs(file_list)

        logger.add(path, format=self.app.config['LOG_FORMAT'], rotation=should_rotate,
                   enqueue=self.app.config['LOG_ENQUEUE'], serialize=self.app.config['LOG_SERIALIZE'],
                   retention=should_retention)

        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions.setdefault("loguru", {})
        app.extensions["loguru"][self] = logger

    def zip_logs(self, file_list):
        """ 超过7天的文件按天打成zip包
        """
        day = datetime.datetime.today().date() - datetime.timedelta(days=7)

        # 设置zip位置
        zip_name = self.app.config['LOG_NAME'] + str(day) + ".zip"

        # 启动zip写入对象
        zp = zipfile.ZipFile(os.path.join(self.app.config['LOG_PATH'], zip_name), "w")
        for tar in file_list:
            zp.write(tar, os.path.basename(tar))

        zp.close()

        for tar in file_list:
            os.remove(tar)