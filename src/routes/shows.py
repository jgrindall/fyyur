"""
Shows controller
"""



from flask import render_template, request, redirect, url_for
from src.models import Artist, Venue, Show
from src.extensions import db
from json import loads
from src.forms import ArtistForm, VenueForm, ShowForm
from src.routes.data.shows import shows as _shows

def setup(app):

    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        # TODO: replace with real venues data.
        return render_template('pages/shows.html', shows = _shows)

    @app.route('/shows/create')
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # TODO: insert form data as a new Show record in the db, instead

        # on successful db insert, flash success
        flash('Show was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')