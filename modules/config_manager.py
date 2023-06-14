#!/usr/bin/env python
# coding=utf-8

import os
import yaml
import shutil

class ConfigError(Exception):
    pass

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join(os.getcwd(), 'config', 'config.yaml')
        self.template_path = os.path.join(os.getcwd(), 'config', 'template.yaml')
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
            error_message = f"配置文件不存在，已通过示例模板创建"
            print(error_message)
            raise ConfigError(error_message)
        else:
            error_message = f"模板配置文件丢失"
            print(error_message)
            raise ConfigError(error_message)

    def get(self, key):
        if self.config is None:
            error_message = "配置文件内没有内容"
            print(error_message)
            raise ConfigError(error_message)
        elif key in self.config:
            return self.config.get(key)
        else:
            error_message =f"配置文件中没有{key}"
            print(error_message)
            raise ConfigError(error_message)



