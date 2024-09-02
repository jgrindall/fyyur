from .artists import setup as setup_artists
from .shows import setup as setup_shows
from .venues import setup as setup_venues
from .errors import setup as setup_errors
from .site import setup as setup_site

def init_routes(app):
    # Register all routes

    #home page
    setup_site(app)

    #venues
    setup_venues(app)

    #shows
    setup_shows(app)

    #artists
    setup_artists(app)

    #errors
    setup_errors(app)
