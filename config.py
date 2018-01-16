#-*- coding: utf-8 -*-

import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# Для поддержки кириллицы
reload(sys)
sys.setdefaultencoding('utf-8')

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SEKRET_KEY') or 'you-will-never-guess' # TODO: сделать SECRET_KEY переменной окружения
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    Debug = True

class TestingConfig(Config):
    Testing = True

class ProductionConfig(Config):
    Debug = False

config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,

          'default': DevelopmentConfig
          }


