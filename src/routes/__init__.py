from .list import setup as setup_list
from .errors import setup as setup_errors
from .site import setup as setup_site

def init_routes(app):
    setup_site(app)
    setup_list(app)
    setup_errors(app)