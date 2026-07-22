import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CHANGE_ME_FOR_LOCAL_DEV_ONLY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///resources.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False