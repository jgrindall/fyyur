"""
Artists controller
"""

from flask import render_template, flash, request, redirect, url_for,abort
from src.models import Artist, Show
from sqlalchemy import text
from src.extensions import db
from src.forms import ArtistForm
import json
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

            # search for artists with upcoming shows whose name contains the search term
            query = db.text("""
                SELECT a.id, a.name, COUNT(s.id) as num_upcoming_shows
                FROM "Artist" a
                LEFT OUTER JOIN "Show" s
                ON a.id = s.artist_id AND s.start_time > NOW()
                WHERE a.name ILIKE :search_term
                GROUP BY a.id
            """)

            result = db.session.execute(query, {'search_term': '%' + search_term + '%'})
            rows = result.fetchall()

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
        query = db.text("""
            SELECT a.*, s.venue_id, s.start_time, v.name as venue_name, v.image_link as venue_image_link
            FROM "Artist" a
            LEFT OUTER JOIN "Show" s
            ON a.id = s.artist_id
            LEFT OUTER JOIN "Venue" v
            ON v.id = s.venue_id
            WHERE a.id = :artist_id
        """)

        result = db.session.execute(query, {'artist_id': int(artist_id)})
        rows = result.fetchall()

        if len(rows) == 0:
            abort(404)
        else:
            row0 = rows[0]

            artist = {
                **(row0._asdict()),
                "genres": (json.loads(row0.genres) if row0.genres else []),
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
        try:
            artist = Artist.query.get(artist_id)
            if artist:
                Artist.edit_using_form_data(artist, request.form)
                db.session.commit()
            else:
                flash('Failed to edit artist')
                abort(404)
        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()           
            if  error == True:
                flash('Failed to edit artist ')
                abort(500)
            else:            
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
        error = False

        try:
            artist = Artist.create_using_form_data(request.form)
            db.session.add(artist)
            db.session.commit()
            artist_id = artist.id
            artist_name = artist.name
            
        except Exception as e:
            print(e)
            error = True
            db.session.rollback()

        finally:
            db.session.close()           
            if  error:
                flash('Failed to create artist')
                abort(500)
            else:            
                flash('Artist ' + artist_name + ' was successfully listed!')
                return redirect(url_for('show_artist', artist_id=artist_id))