
from flask import render_template, request, flash, redirect, url_for, abort
from src.models import Venue, Show
from src.extensions import db
from src.forms import VenueForm
import json
from datetime import datetime

def setup(app):
    
    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():

        query = db.text("""
            select v.id, v.name, v.state, v.city, count(*)  as num_upcoming_shows
            from "Venue" v 
            join "Show" s
            on v.id=s.venue_id
            WHERE s.start_time > NOW()
            group by v.id
        """)


        result = db.session.execute(query)
        rows = result.fetchall()

        areas = {}

        for row in rows:
            key = row.city + ":" + row.state
            venue = {
                "id": row.id,
                "name": row.name,
                "num_upcoming_shows": row.num_upcoming_shows
            }

            if key in areas:
                areas[key]['venues'].append(venue)
            else:
                areas[key] = {
                    "city": row.city,
                    "state": row.state,
                    "venues": [
                        venue
                    ]
                }

        return render_template('pages/venues.html', areas=areas.values())

    


    
    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        search_term = request.form.get('search_term', '').strip()
        if(search_term == ""):
            results = {
                "count": 0,
                "data": []
            }
        else:

            query = db.text("""
                select v.id, v.name, v.state, v.city, count(*)  as num_upcoming_shows
                from "Venue" v 
                join "Show" s
                on v.id=s.venue_id
                WHERE s.start_time > NOW()
                AND a.name ILIKE :search_term
                GROUP BY a.id, a.name
            """)

            result = db.session.execute(query, {'search_term': '%' + search_term + '%'})
            rows = result.fetchall()

            def to_dict(row):
                return {
                    "id": row.id,
                    "name": row.name,
                    "num_upcoming_shows": row.num_upcoming_shows
                }

            results = {
                "count": len(rows),
                "data": [to_dict(row) for row in rows]
            }
            return render_template('pages/search_venues.html', results=results, search_term=search_term)
    

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):

        query = db.text("""
            select v.*, s.artist_id, s.start_time, a.name as artist_name, a.image_link as artist_image_link
            from "Venue" v 
            join "Show" s
            on v.id = s.venue_id
            join "Artist" a
            on a.id=s.artist_id
            where v.id = :venue_id
        """)

        result = db.session.execute(query, {'venue_id': venue_id})
        rows = result.fetchall()

        if len(rows) == 0:
            abort(404)
        else:
            row0 = rows[0]

            venue = {
                "id": row0.id,
                "name": row0.name,
                "city": row0.city,
                "state": row0.state,
                "address": row0.address,
                "phone": row0.phone,
                "image_link": row0.image_link,
                "facebook_link": row0.facebook_link,
                "website": row0.website,
                "seeking_talent": row0.seeking_talent,
                "seeking_description": row0.seeking_description,
                "genres": (json.loads(row0.genres) if row0.genres else []),
                "upcoming_shows": [],
                "past_shows": [],
                "upcoming_shows_count": 0,
                "past_shows_count": 0
            }

            for row in rows:
                show = {
                    "artist_id": row.artist_id,
                    "artist_name": row.artist_name,
                    "artist_image_link": row.artist_image_link,
                    "start_time": Show.time_to_string(row.start_time)
                }
                if(row.start_time > datetime.now()):
                    venue['upcoming_shows'].append(show)
                    venue['upcoming_shows_count'] += 1
                else:
                    venue['past_shows'].append(show)
                    venue['past_shows_count'] += 1

        return render_template('pages/show_venue.html', venue=venue)

    


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
