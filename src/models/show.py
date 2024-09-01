from ..extensions import db

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    artist = db.relationship('Artist', backref = db.backref('shows', cascade="all, delete-orphan", lazy=True))
    venue = db.relationship('Venue', backref = db.backref('shows', cascade="all, delete-orphan", lazy=True))
