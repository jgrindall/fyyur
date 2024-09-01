import os

SECRET_KEY = os.urandom(32)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:p0stgr3sM1l0!@localhost:5432/fyyur'
