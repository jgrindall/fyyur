
from flask import render_template, request, flash, redirect, url_for, abort
from src.models import Venue
from src.extensions import db
from src.forms import VenueForm

def setup(app):
    
    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        _venues = Venue.query.all()

        # TODO: replace with real venues data.
        # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
        return render_template('pages/venues.html', areas=_venues);

    


    
    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        search_term = request.form.get('search_term', '').strip()
        if(search_term == ""):
            results = {
                "count": 0,
                "data": []
            }
        else:
            venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
            results = {
                "count": len(venues),
                "data": [venue.to_dict() for venue in venues]
            }
            return render_template('pages/search_venues.html', results=results, search_term=search_term)
        





    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        venue = Venue.query.get(venue_id)
        venue_json = venue.to_dict()
        return render_template('pages/show_venue.html', venue=venue_json)

    


    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():

        error = False
        venue_name = None

        try:
            venue = Venue.create_using_form_data(request.form)
            db.session.add(venue)
            db.session.commit()
            venue_name = venue.name
            
        except Exception as e:
            print(e)
            error = True
            db.session.rollback()

        finally:
            db.session.close()           
            if  error == True:
                abort(400)
            else:            
                flash('Venue ' + venue_name + ' was successfully listed!')
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
        venue = Venue.query.get(venue_id)
        venue_json = venue.to_dict()
        form = VenueForm(obj=venue_json)
        return render_template('forms/edit_venue.html', form=form, venue=venue)




    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
        try:
            venue = Venue.query.get(venue_id)
            if venue:
                Venue.edit_using_form_data(venue, request.form)
                db.session.commit()

            else:
                abort(400)
        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()           
            if  error == True:
                abort(400)
            else:            
                return redirect(url_for('show_venue', venue_id=venue_id))
