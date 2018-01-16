#-*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()
# Фабричная функция (создаем экземпляр приложения)
def create_app(config_name):
    app = Flask(__name__)  # Создаем приложение
    # Настраиваем приложение: Импортируем настройки из config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # Иницируем приложение

    bootstrap.init_app(app)

    # Зарегистрировали макеты
    from main import main
    app.register_blueprint(main)
    from api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    return app
