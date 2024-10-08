"""
Shows controller
"""

from flask import render_template, request, flash, abort
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

        statusCode = 200
        show_id = None

        try:
            form = ShowForm(request.form, meta={"csrf": False})
            if(form.validate()):
                show = Show.create_using_form_data(form)
                db.session.add(show)
                db.session.commit()
                show_id = show.id
            else:
                flash('Invalid show ' + str(form.errors))
                statusCode = 400
            
        except Exception as e:
            db.session.rollback()
            print(e, flush=True)
            flash('Error creating show ' + str(e))
            statusCode = 500
            
        finally:
            db.session.close()
            if  statusCode != 200:
                abort(statusCode)
            else:
                flash('Show id ' + str(show_id) + ' was successfully listed!')
                return render_template('pages/home.html')

