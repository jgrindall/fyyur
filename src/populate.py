from src.models import Artist, Venue, Show
from src.extensions.database import db
import json
from datetime import datetime

#default data to be added to the database

artist0 = {
    "name": "Guns N Petals",
    "genres": [
        "Rock n Roll"
    ],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
}

artist1 = {
    "name": "Matt Quevedo",
    "genres": [
        "Jazz"
    ],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
}

artist2 = {
    "name": "The Wild Sax Band",
    "genres": [
        "Jazz", 
        "Classical"
    ],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
}

venue0 = {
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
}

venue1 = {
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
}

venue2 = {
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
}

shows = [
    {
        "venue_name": "The Musical Hop",
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    },
    {
        "venue_name": "Park Square Live Music & Coffee",
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    },
    {
        "venue_name": "Park Square Live Music & Coffee",
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, 
    {
        "venue_name": "Park Square Live Music & Coffee",
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, 
    {
        "venue_name": "Park Square Live Music & Coffee",
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }
]

def _make_artist(data):
    return Artist(
       name = data['name'],
       genres = json.dumps(data['genres']),
       city = data['city'],
       state = data['state'],
       phone = data['phone'],
       image_link = data.get('image_link', ''),
       facebook_link = data.get('facebook_link', ''),
       website = data.get('website', ''),
       seeking_venue = data.get('seeking_venue', False),
       seeking_description = data.get('seeking_description', '')
    )

def _make_venue(data):
    return Venue(
       name = data['name'],
       genres = json.dumps(data['genres']),
       address = data['address'],
       city = data['city'],
       state = data['state'],
       phone = data['phone'],
       image_link = data.get('image_link', ''),
       facebook_link = data.get('facebook_link', ''),
       website = data.get('website', ''),
       seeking_talent = data.get('seeking_talent', False),
       seeking_description = data.get('seeking_description', '')
    )

def _make_show(data):
    # find the artist and venue
    venue = Venue.query.filter_by(name=data['venue_name']).first()
    artist = Artist.query.filter_by(name=data['artist_name']).first()
    return Show(
        venue_id = venue.id,
        artist_id = artist.id,
        start_time = Show.string_to_time(data['start_time'])
    )    


def _add_artists():
    first_artist = Artist.query.first()
    if not first_artist:
        error = False
        num = 0
        print("adding artists...", flush=True)
        try:
            for artist_data in [artist0, artist1, artist2]:
                artist = _make_artist(artist_data)
                db.session.add(artist)
                num += 1
            db.session.commit()
        except Exception as e:
            print(e, flush=True)
            error = True
            db.session.rollback()

        finally:
            print("success: ", not error, num, flush=True)
            db.session.commit()
            db.session.close()


def _add_venues():
    first_venue = Venue.query.first()
    if not first_venue:
        error = False
        num = 0
        print("adding venues...", flush=True)
        try:
            for venue_data in [venue0, venue1, venue2]:
                venue = _make_venue(venue_data)
                db.session.add(venue)
                num += 1
            db.session.commit()
        except Exception as e:
            print(e, flush=True)
            error = True
            db.session.rollback()

        finally:
            print("success: ", not error, num, flush=True)
            db.session.commit()
            db.session.close()


def _add_shows():
    first_show = Show.query.first()
    if not first_show:
        error = False
        num  = 0
        print("adding shows...", flush=True)
        try:
            for show_data in shows:
                show = _make_show(show_data)
                db.session.add(show)
                num += 1    
                db.session.commit()
        except Exception as e:
            print(e, flush=True)
            error = True
            db.session.rollback()

        finally:
            print("success: ", not error, num, flush=True)
            db.session.commit()
            db.session.close()


def populate_db():
    print("populating db...", flush=True)

    _add_artists()
    _add_venues()
    _add_shows()

    print("db populated", flush=True)
