import os
from dotenv import dotenv_values

config = dotenv_values(".env")
POSTGRES_PWD = config['POSTGRES_PWD']

SECRET_KEY = os.urandom(32)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + POSTGRES_PWD + '@localhost:5432/fyyur'
