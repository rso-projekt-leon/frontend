import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DOWNLOAD_FILE = '/home/leons/data-platform/frontend/data'

    # UPLOAD_URL = 'http://localhost:8081/v1/upload'
    # DATA_URL = 'http://localhost:8083/v1/datasets'
    # STORAGE_URL = 'http://localhost:8082/v1/files'
    UPLOAD_URL = 'http://35.195.92.163/data-upload/v1/upload'
    DATA_URL = 'http://35.195.92.163/data-catalog/v1/datasets'
    STORAGE_URL = 'http://35.195.92.163/data-storage/v1/files'