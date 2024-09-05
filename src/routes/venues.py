
from flask import render_template, request, flash, redirect, url_for, abort
from src.models import Venue, Show, Artist
from src.extensions import db
from src.forms import VenueForm
import json
from sqlalchemy import  func
from datetime import datetime

def setup(app):
    
    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        
        '''
        Rewrite the following query to use SQLAlchemy ORM
        query = db.text("""
            SELECT v.id, v.name, v.state, v.city, count(s.id) as num_upcoming_shows
            FROM "Venue" v 
            LEFT OUTER JOIN "Show" s
            ON v.id = s.venue_id
            AND s.start_time > NOW()
            GROUP BY v.id
        """)
        '''

        query = db.session.query(
            Venue.id,
            Venue.name,
            Venue.state,
            Venue.city,
            func.count(Show.id).label('num_upcoming_shows')
        ).outerjoin(
            Show, 
            (Venue.id == Show.venue_id) & (Show.start_time > func.now())
        ).group_by(
            Venue.id
        )

        rows = query.all()

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

            search_term_wildcard = '%' + search_term + '%'

            '''
            Rewrite the following query to use SQLAlchemy ORM
            query = db.text("""
                SELECT v.id, v.name, v.state, v.city, count(s.id) as num_upcoming_shows
                FROM "Venue" v 
                LEFT OUTER join "Show" s
                ON v.id = s.venue_id
                AND s.start_time > NOW()
                WHERE v.name ILIKE :search_term
                GROUP BY v.id
            """)
            '''

            query = db.session.query(
                Venue.id,
                Venue.name,
                Venue.state,
                Venue.city,
                func.count(Show.id).label('num_upcoming_shows')
            ).outerjoin(
                Show, 
                (Venue.id == Show.venue_id) & (Show.start_time > func.now())
            ).filter(
                Venue.name.ilike(search_term_wildcard)
            ).group_by(
                Venue.id
            )

            rows = query.all()
            
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

        '''

        Rewrite the following query to use SQLAlchemy ORM

        query = db.text("""
            SELECT v.*, s.artist_id, s.start_time, a.name as artist_name, a.image_link as artist_image_link
            FROM "Venue" v 
            LEFT OUTER JOIN "Show" s
            ON v.id = s.venue_id
            LEFT OUTER JOIN "Artist" a
            ON a.id=s.artist_id
            WHERE v.id = :venue_id
        """)
        '''
        
        query = db.session.query(
            *Venue.__table__.columns, 
            Show.artist_id,
            Show.start_time,
            Artist.name.label('artist_name'),
            Artist.image_link.label('artist_image_link'),
        ).outerjoin(
            Show, 
            (Venue.id == Show.venue_id)
        ).outerjoin(
            Artist, 
            Artist.id == Show.artist_id
        ).filter(
            Venue.id == venue_id
        )

        rows = query.all()
        
        if len(rows) == 0:
            abort(404)
        else:
            row0 = rows[0]

            venue = {
                **(row0._asdict()),
                "genres": (json.loads(row0.genres) if row0.genres else []),
                "upcoming_shows": [],
                "past_shows": [],
                "upcoming_shows_count": 0,
                "past_shows_count": 0
            }

            for row in rows:
                if(row.artist_id != None):
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
                flash('Failed to create venue')
                abort(500)
            else:            
                flash('Venue ' + venue_name + ' was successfully listed!')
                return render_template('pages/home.html')

    
    
    
    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
        try:
            venue = Venue.query.get(venue_id)
            db.session.delete(venue)
            db.session.commit()
       
        except Exception as e:
            print(e)
            error = True
            db.session.rollback()

        finally:
            db.session.close()           
            if  error == True:
                flash('Venue deletion failed')
                abort(500)
            else:            
                flash('Venue was successfully deleted!')
                return "ok"
    




    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
        venue = Venue.query.get(venue_id)
        venue_json = venue.to_dict()
        form = VenueForm(obj=venue)
        return render_template('forms/edit_venue.html', form=form, venue=venue_json)




    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
        try:
            venue = Venue.query.get(venue_id)
            if venue:
                Venue.edit_using_form_data(venue, request.form)
                db.session.commit()

            else:
                flash('Venue edit failed')
                abort(404)
        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()           
            if  error == True:
                flash('Venue edit failed')
                abort(500)
            else:            
                return redirect(url_for('show_venue', venue_id=venue_id))
