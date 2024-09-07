from ..extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500), nullable=True)

    seeking_venue = db.Column(db.Boolean, default=False, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,

            "image_link": self.image_link or "",
            "facebook_link": self.facebook_link or "",
            "seeking_venue": self.seeking_venue or False,
            "seeking_description": self.seeking_description or "",
            "website": self.website or "",
            "genres": self.genres
        }
    
    @staticmethod
    def edit_using_form_data(artist, form):
        artist.name = form.data['name']
        artist.city = form.data['city']
        artist.state = form.data['state']
        artist.phone = form.data['phone']
        artist.image_link = form.data['image_link']
        artist.facebook_link = form.data['facebook_link']
        artist.website = form.data['website']
        artist.seeking_venue = form.data['seeking_venue']
        artist.seeking_description = form.data['seeking_description']
        artist.genres = form.data['genres']


    @staticmethod
    def create_using_form_data(form):
        artist = Artist(
            name = form.data['name'],
            city = form.data['city'],
            state = form.data['state'],
            phone = form.data['phone'],
            genres = form.data['genres'],
            image_link = form.data['image_link'],
            facebook_link = form.data['facebook_link'],
            seeking_venue = form.data['seeking_venue'],
            seeking_description = form.data['seeking_description'],
            website = form.data['website']
        )
        return artist