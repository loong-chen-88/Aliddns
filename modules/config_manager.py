#!/usr/bin/env python
# coding=utf-8

import os
import yaml
import shutil


class ConfigError(Exception):
    pass


class ConfigManager:
    def __init__(self):
        self.file_path = os.path.dirname(os.path.dirname(__file__))
        self.config_path = os.path.join(
            self.file_path, 'config', 'config.yaml')
        self.template_path = os.path.join(
            self.file_path, 'config', 'template.yaml')
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                return config
        else:
            self._create_configfile()
            return self._load_config()

    def _create_configfile(self):
        if os.path.exists(self.template_path):
            shutil.copy(self.template_path, self.config_path)
            error_message = f"没有配置文件,已通过示例模板创建:'{self.config_path}',修改后再运行"
            raise ConfigError(error_message)
        else:
            error_message = f"示例模板:'{self.template_path}'丢失,从源文件重新获取"

            raise ConfigError(error_message)

    def get(self, key):
        if self.config is None:
            error_message = f"配置文件:'{self.config_path}'内没有内容"
            raise ConfigError(error_message)
        elif key in self.config:
            return self.config.get(key)
        else:
            error_message = f"配置文件:'{self.config_path}'内没有'{key}'"
            raise ConfigError(error_message)
