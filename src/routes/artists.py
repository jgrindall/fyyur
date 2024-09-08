"""
Artists controller
"""

from flask import render_template, flash, request, redirect, url_for, abort
from src.models import Artist, Show, Venue
from sqlalchemy import  func
from src.extensions import db
from src.forms import ArtistForm
from datetime import datetime


def setup(app):

    # view all artists - id and name
    @app.route('/artists')
    def artists():
        artists = Artist.query.all()
        return render_template('pages/artists.html', artists=artists)

    


    
    # search artists. Return count of search results and data (including num_upcoming_shows)
    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        
        search_term = request.form.get('search_term', '').strip()

        if(search_term == ""):
            results = {
                "count": 0,
                "data": []
            }
        else:

            search_term_wildcard = '%' + search_term + '%'

            # search for artists with upcoming shows whose name contains the search term
           
            query = db.session.query(
                Artist.id, 
                Artist.name, 
                func.count(Show.id).label('num_upcoming_shows')
            ).outerjoin(
                Show, 
                (Artist.id == Show.artist_id) & (Show.start_time > func.now())
            ).filter(
                Artist.name.ilike(search_term_wildcard)
            ).group_by(
                Artist.id
            )

            rows = query.all()

            def to_dict(row):
                return {
                    **(row._asdict()),
                    "num_upcoming_shows": row.num_upcoming_shows
                }

            results = {
                "count": len(rows),
                "data": [to_dict(row) for row in rows]
            }
            return render_template('pages/search_artists.html', results=results, search_term=search_term)

    


    
    # view artist details
    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):

        # join Artist, Show, and Venue tables to get artist details and show details
        
        query = db.session.query(
            *Artist.__table__.columns, 
            Show.venue_id,
            Show.start_time,
            Venue.name.label('venue_name'),
            Venue.image_link.label('venue_image_link'),
        ).outerjoin(
            Show, 
            (Artist.id == Show.artist_id)
        ).outerjoin(
            Venue, 
            Venue.id == Show.venue_id
        ).filter(
            Artist.id == artist_id
        )

        rows = query.all()

        if len(rows) == 0:
            abort(404)
        else:
            row0 = rows[0]

            print(row0, flush=True)

            artist = {
                **(row0._asdict()),
                "upcoming_shows": [],
                "past_shows": [],
                "upcoming_shows_count": 0,
                "past_shows_count": 0
            }

            now = datetime.now()

            for row in rows:
                if(row.venue_id != None):
                    show = {
                        "venue_id": row.venue_id,
                        "venue_name": row.venue_name,
                        "venue_image_link": row.venue_image_link,
                        "start_time": Show.time_to_string(row.start_time)
                    }
                    if(row.start_time > now):
                        artist['upcoming_shows'].append(show)
                        artist['upcoming_shows_count'] += 1
                    else:
                        artist['past_shows'].append(show)
                        artist['past_shows_count'] += 1

        return render_template('pages/show_artist.html', artist=artist)

    
    
    #  edit artist GET
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        artist = Artist.query.get(artist_id)
        artist_json = artist.to_dict()
        form = ArtistForm(obj=artist)
        return render_template('forms/edit_artist.html', form=form, artist=artist_json)

    
    # edit artist using form submission POST
    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        statusCode = 200
        try:
            artist = Artist.query.get(artist_id)
            if artist:
                form = ArtistForm(request.form, meta={"csrf": False})
                if form.validate():
                    Artist.edit_using_form_data(artist, form)
                    db.session.commit()
                else:
                    flash('Invalid form data ' + str(form.errors))
                    statusCode = 400
            else:
                flash('Artist not found')
                statusCode = 404
        except Exception as e:
            print(e, flush=True)
            statusCode = 500
            flash('Error editing artist ' + str(e))
            db.session.rollback()

        finally:
            db.session.close()           
            if  statusCode != 200:
                abort(statusCode)
            else:
                flash('Artist successfully edited')
                return redirect(url_for('show_artist', artist_id=artist_id))




    #  Create Artist GET
    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    
    # Create Artist POST
    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():

        artist_id = None
        artist_name = None
        statusCode = 200

        try:
            form = ArtistForm(request.form, meta={"csrf": False})
            if form.validate():
                artist = Artist.create_using_form_data(form)
                db.session.add(artist)
                db.session.commit()
                artist_id = artist.id
                artist_name = artist.name
            else:
                flash('Invalid form data ' + str(form.errors))
                statusCode = 400
            
        except Exception as e:
            print(e, flush=True)
            statusCode = 500
            flash('Error creating artist ' + str(e))
            db.session.rollback()

        finally:
            db.session.close()           
            if  statusCode != 200:
                abort(statusCode)
            else:            
                flash('Artist ' + artist_name + ' was successfully listed!')
                return redirect(url_for('show_artist', artist_id=artist_id))