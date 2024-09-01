

"""
Artists controller
"""

from flask import render_template, flash, request, redirect, url_for
from src.models import Artist, Venue
from src.extensions import db
from json import loads
from src.forms import ArtistForm, VenueForm, ShowForm
from src.routes.data.artists import artists, search, data1, data2, data3, artist0

def setup(app):

    @app.route('/artists')
    def artists():
        artists = Artist.query.all()
        return render_template('pages/artists.html', artists=artists)

    
    
    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        search_term = request.form.get('search_term', '').strip()
        if(search_term == ""):
            return render_template('pages/search_artists.html', results=[], search_term=request.form.get('search_term', ''))
        else:
            artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
            results = {
                "count": len(artists),
                "data": [artist.to_dict() for artist in artists]
            }
            return render_template('pages/search_artists.html', results=results, search_term=request.form.get('search_term', ''))

    
    
    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
        artist = Artist.query.get(artist_id)
        artist_json = artist.to_dict()
        return render_template('pages/show_artist.html', artist=artist_json)

    
    
    #  Update
    #  ----------------------------------------------------------------
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        artist = Artist.query.get(artist_id)
        artist_json = artist.to_dict()
        form = ArtistForm(obj=artist)
        return render_template('forms/edit_artist.html', form=form, artist=artist_json)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):

        print("UPDATE")
        print(request.form)
        
        #request.form['seeking_venue'] = True if request.form.get('seeking_venue') == 'y' else False

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


  