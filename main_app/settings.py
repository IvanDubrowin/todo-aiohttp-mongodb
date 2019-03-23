import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = '/static'

TEMPLATES_ROOT = os.path.join(BASE_DIR, 'templates')

SITE_HOST = '127.0.0.1'

SITE_PORT = 8080

SECRET_KEY = 'secret'

MONGO_HOST = 'mongodb://mongodb:27017/'

MONGO_DB_NAME = 'mongo_database'

TASK_COLLECTION = 'tasks'

USER_COLLECTION = 'users'

DEBUG = False
