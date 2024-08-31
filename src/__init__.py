from flask import Flask
from flask_migrate import Migrate
from src.extensions import db
from src.config import DEBUG, SQLALCHEMY_DATABASE_URI
from src.routes import init_routes
from src.filters import init_filters

def create_app():
    app = Flask("fyyur")

    #todo - use "from config"

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['EXPLAIN_TEMPLATE_LOADING'] = DEBUG
    app.debug = DEBUG

    app.app_context().push()
    
    db.init_app(app)

    Migrate(app, db)

    init_routes(app)
    init_filters(app)

    return app


"""
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
"""