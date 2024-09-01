"""
Shows controller
"""



from flask import render_template, request, flash, redirect, url_for
from src.models import Artist, Venue, Show
from src.extensions import db
from json import loads
from src.forms import ArtistForm, VenueForm, ShowForm
from src.routes.data.shows import shows as _shows

def setup(app):

    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
        shows = Show.query.all()

        def show_to_dict(show):
            return {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": Show.time_to_string(show.start_time)
            }

        _shows = [show_to_dict(show) for show in shows]

        return render_template('pages/shows.html', shows = _shows)

    @app.route('/shows/create')
    def create_shows():
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        venue_id = int(request.form.get('venue_id'))
        artist_id = int(request.form.get('artist_id'))
        start_time = request.form.get('start_time')

        try:
            show = Show(
                venue_id = venue_id,
                artist_id = artist_id,
                start_time = Show.string_to_time(start_time)
            )
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('An error occurred. Show could not be listed.')
            return render_template('pages/home.html')
        finally:
            db.session.close()
