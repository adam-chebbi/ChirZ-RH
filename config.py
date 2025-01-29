import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chebbi.exe'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/cv_jd_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False