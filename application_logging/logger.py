import datetime as dt
import logging
import os


class App_Logger:
    def __init__(self):
        self.CODE_DIR = os.getcwd()
        self.logger = None
        self.handler = None

    def create_logger(self, logger_name, logpath):
        self.handler = logging.FileHandler(logpath)
        formatter = logging.Formatter(
            '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d (Line No.)} %(levelname)s - %(message)s',
            '%m-%d %H:%M:%S')
        self.handler.setFormatter(formatter)
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
        return self.logger

    def create_success_logger(self,logpath):
        self.logpath = logpath
        success_logger = self.create_logger('success_logger', logpath)
        return success_logger

    def create_failure_logger(self,logpath):
        self.logpath = logpath
        failure_logger = self.create_logger('failure_logger', logpath)
        return failure_logger


   