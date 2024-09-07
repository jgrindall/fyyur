import os

POSTGRES_PWD="thisismypassword"

SECRET_KEY = os.urandom(32)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + POSTGRES_PWD + '@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS  = False
