from flask import Flask
from flask_migrate import Migrate
from src.extensions import db
from src.config import DEBUG, SQLALCHEMY_DATABASE_URI

def create_app():
    app = Flask("fyyur")

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['EXPLAIN_TEMPLATE_LOADING'] = DEBUG
    app.debug = DEBUG

    app.app_context().push()
    
    db.init_app(app)

    migrate = Migrate(app, db)

    #init_routes(app)
    #init_filters(app)

    return app
