import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_URL = 'http://localhost:8081/v1/upload'
    DATA_URL = 'http://localhost:8083/v1/datasets'