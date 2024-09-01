
from flask import render_template, request, redirect, url_for
from src.models import Artist, Venue
from src.extensions import db
from json import loads
from src.forms import ArtistForm, VenueForm, ShowForm
from src.routes.data.artists import artists, search, data1, data2, data3, artist0

def setup(app):

    #  Artists
    #  ----------------------------------------------------------------
    @app.route('/artists')
    def artists():
        return render_template('pages/artists.html', artists=artists)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        return render_template('pages/search_artists.html', results=search, search_term=request.form.get('search_term', ''))

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
        # shows the artist page with the given artist_id
        # TODO: replace with real artist data from the artist table, using artist_id
        data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
        return render_template('pages/show_artist.html', artist=data)

    #  Update
    #  ----------------------------------------------------------------
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        form = ArtistForm()
        # TODO: populate form with fields from artist with ID <artist_id>
        return render_template('forms/edit_artist.html', form=form, artist=artist0)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        # TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes
        return redirect(url_for('show_artist', artist_id=artist_id))

    

    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():
        # called upon submitting the new artist listing form
        # TODO: insert form data as a new Venue record in the db, instead
        # TODO: modify data to be the data object returned from db insertion

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        return render_template('pages/home.html')


  