
from flask import render_template, request, redirect, url_for
from src.models import Artist, Venue
from src.extensions import db
from json import loads
from src.forms import ArtistForm, VenueForm, ShowForm
from src.routes.data.shows import shows

def setup(app):

    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        # TODO: replace with real venues data.
        return render_template('pages/shows.html', shows = shows)

  