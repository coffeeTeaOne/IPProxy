# coding = "utf-8"
import logging
import re
import sys
import time
import os

from ProxyLog.logpath import PathLog

DEFAULT_LOG_LEVEL = logging.INFO
# 默认日志格式
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
# 默认时间格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
# 默认日志文件名称
rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# 默认Python日志存放地址
# DEFAULT_LOG_DIR = "/tmp/logs/python"
DEFAULT_LOG_DIR = PathLog().log_path()
# datashufflepy 项目日志

# 普通池
DEFAULT_LOG_FILENAME = DEFAULT_LOG_DIR + 'common.agentpool.log.' + rq
# 微信池
# DEFAULT_LOG_FILENAME = DEFAULT_LOG_DIR + 'wechat.agentpool.log.' + rq
# print(DEFAULT_LOG_FILENAME)


class ProxyLogger(object):

    def __init__(self):
        self._logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=DEFAULT_LOG_FMT, datefmt=DEFUALT_LOG_DATEFMT)
        if not self._logger.handlers:
            self._logger.addHandler(self._get_file_handler(DEFAULT_LOG_FILENAME))

        # self._logger.addHandler(self._get_console_handler())
            self._logger.setLevel(DEFAULT_LOG_LEVEL)
            self.base_dir = os.path.dirname(os.getcwd())

    def _get_file_handler(self, filename):
        try:
            filehandler = logging.FileHandler(filename=filename, encoding="utf-8")
        except FileNotFoundError:
            os.mkdir(DEFAULT_LOG_DIR + "/")
            filehandler = logging.FileHandler(filename=filename, encoding="utf-8")

        filehandler.setFormatter(self.formatter)
        return filehandler

    def _get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    @property
    def logger(self):
        return self._logger


if __name__ == '__main__':
    logger = ProxyLogger().logger
    # logger.info('aaaa')
    # logger.debug('this is a logger debug message')
    # logger.info('this is a logger info message')
    # logger.warning('this is a logger warning message')
    # logger.error('this is a logger error message')
    # logger.critical('this is a logger critical message')
    logger.handlers.clear()
