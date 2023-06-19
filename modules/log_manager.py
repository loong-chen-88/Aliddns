#!/usr/bin/env python
# coding=utf-8

import os
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self):
        self.app_path = os.path.dirname(os.path.dirname(__file__))
        self.log_path = os.path.join(self.app_path, 'logs')
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        self.log_file = os.path.join(
            self.log_path, datetime.datetime.now().strftime("%Y%m%d.log"))
        self.logger = logging.getLogger("log_manager")
        self.logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s--%(levelname)s: %(message)s")
        file_handler = TimedRotatingFileHandler(
            self.log_file, when="midnight", interval=1, backupCount=90, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)
