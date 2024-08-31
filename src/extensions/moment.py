from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from forms import *

def setup(app):
    moment = Moment(app)
    