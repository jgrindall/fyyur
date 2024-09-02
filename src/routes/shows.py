"""
Shows controller
"""

from flask import render_template, request, flash
from src.models import Show
from src.extensions import db
from src.forms import ShowForm

def setup(app):

    
    # view all shows
    @app.route('/shows')
    def shows():
        all_shows = Show.query.all()

        def show_to_dict(show):
            return {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": Show.time_to_string(show.start_time)
            }

        shows = [show_to_dict(show) for show in all_shows]

        return render_template('pages/shows.html', shows = shows)




    @app.route('/shows/create')
    def create_shows():
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)



    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        try:
            show = Show.create_using_form_data(request.form)
            print("add show", show, flush=True)
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
            
        except Exception as e:
            db.session.rollback()
            print(e, flush=True)
            flash('An error occurred. Show could not be listed.')
            
        finally:
            db.session.close()
            return render_template('pages/home.html')
