from ..extensions import db
from datetime import datetime

# the format of the datetime string that is sent to the client
datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'

class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    artist = db.relationship('Artist', backref = db.backref('shows', cascade="all, delete-orphan", lazy=True))
    venue = db.relationship('Venue', backref = db.backref('shows', cascade="all, delete-orphan", lazy=True))

    @staticmethod
    def create_using_form_data(form):
        venue_id = form.data['venue_id']
        artist_id = form.data['artist_id']
        start_time = form.data['start_time']
        
        show = Show(
            venue_id = venue_id,
            artist_id = artist_id,
            start_time = start_time
        )
        return show

    @staticmethod
    def time_to_string(time):
        return time.strftime(datetime_format)
    
    @staticmethod
    def string_to_time(s):
        return datetime.strptime(s, datetime_format)