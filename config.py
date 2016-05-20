#!/usr/bin/env python
# encoding: utf-8


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5q+B8pJdP8FUJ3yPtG/m'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 2000
    FLASK_PER_PAGE = 20

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Shanghai'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    #  REDIS_HOST = os.getenv('REDIS_HOST', '172.16.0.35')
    #  REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    #  CELERY_BROKER_URL = 'redis://{0}:{1}/0'.format(REDIS_HOST, REDIS_PORT)
    #  CELERY_RESULT_BACKEND = 'redis://{0}:{1}/0'.format(REDIS_HOST, REDIS_PORT)

    MYSQL_HOST = os.getenv('MYSQL_HOST', '172.16.0.35')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_USER = os.getenv('MYSQL_USER', 'viktor')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'viktor')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'viktor')
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
        MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE,
    )


config = {
    'default': DevelopmentConfig,
}
