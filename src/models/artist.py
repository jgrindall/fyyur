from ..extensions import db
import json
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
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

            # json
            "genres": json.loads(self.genres) if self.genres else []
        }
    
    @staticmethod
    def edit_using_form_data(artist, form):
        artist.name = form.get('name', artist.name)
        artist.city = form.get('city', artist.city)
        artist.state = form.get('state', artist.state)
        artist.phone = form.get('phone', artist.phone)
        artist.image_link = form.get('image_link', artist.image_link)
        artist.facebook_link = form.get('facebook_link', artist.facebook_link)
        artist.website = form.get('website', artist.website) 
        artist.seeking_venue = form.get('seeking_venue', artist.seeking_venue)
        artist.seeking_description = form.get('seeking_description', artist.seeking_description)
        artist.genres = json.dumps(form.get('genres', artist.genres))


    @staticmethod
    def create_using_form_data(form):
        artist = Artist(
            name = form['name'],
            city = form['city'],
            state = form['state'],
            phone = form['phone'],
            genres = json.dumps(form.getlist('genres')),
            image_link = form.get('image_link', ''),
            facebook_link = form.get('facebook_link', ''),
            seeking_venue = form.get('seeking_venue', False),
            seeking_description = form.get('seeking_description', ''),
            website = form.get('website', '')
        )
        return artist