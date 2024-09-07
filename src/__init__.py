from flask import Flask
from flask_migrate import Migrate
from src.extensions import db
from src.routes import init_routes
from src.filters import init_filters
from src.populate import populate_db
import src.config as config
import sys

v0 = sys.version_info[0:1][0]
v1 = sys.version_info[1:2][0]

if(v0 != 3 or v1 < 12):
    print("Please use Python 3.12 or higher", flush=True)
    sys.exit(1)

def create_app():
    app = Flask("fyyur")

    app.config.from_object(config)

    app.app_context().push()
    
    db.init_app(app)
    Migrate(app, db)

    init_routes(app)
    init_filters(app)

    return app
