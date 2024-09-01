
from flask import render_template, request, redirect, url_for
from src.models import Artist, Venue
from src.extensions import db
from json import loads
from src.forms import ArtistForm, VenueForm, ShowForm
from src.routes.data.venues import venues as _venues
from src.routes.data.venue import data1, data2, data3, venue0, search
def setup(app):
    
    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        # TODO: replace with real venues data.
        #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
        return render_template('pages/venues.html', areas=_venues);

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        search_term = request.form.get('search_term', '')
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        return render_template('pages/search_venues.html', results=search, search_term=search_term)

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        # shows the venue page with the given venue_id
        # TODO: replace with real venue data from the venues table, using venue_id
        data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
        return render_template('pages/show_venue.html', venue=data)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
        # TODO: insert form data as a new Venue record in the db, instead
        # TODO: modify data to be the data object returned from db insertion

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
        # TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        return None

    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
        form = VenueForm()
        # TODO: populate form with values from venue with ID <venue_id>
        return render_template('forms/edit_venue.html', form=form, venue=venue0)

    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
        # TODO: take values from the form submitted, and update existing
        # venue record with ID <venue_id> using the new attributes
        return redirect(url_for('show_venue', venue_id=venue_id))

