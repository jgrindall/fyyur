from ..extensions import db
import json

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))

    seeking_talent = db.Column(db.Boolean, default=False, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    website = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "address": self.address,
            "phone": self.phone,

            # nullable
            "image_link": self.image_link or "",
            "facebook_link": self.facebook_link or "",
            "seeking_talent": self.seeking_talent or False,
            "seeking_description": self.seeking_description or "",
            "website": self.website or "",

            # json
            "genres": json.loads(self.genres) if self.genres else []
        }
    
    @staticmethod
    def edit_using_form_data(venue, form):
        venue.name = form.get('name', venue.name)
        venue.city = form.get('city', venue.city)
        venue.state = form.get('state', venue.state)
        venue.address = form.get('address', venue.address)
        venue.phone = form.get('phone', venue.phone)
        venue.image_link = form.get('image_link', venue.image_link)
        venue.facebook_link = form.get('facebook_link', venue.facebook_link)
        venue.seeking_talent = form.get('seeking_talent', venue.seeking_talent)
        venue.seeking_description = form.get('seeking_description', venue.seeking_description)
        venue.website = form.get('website', venue.website)
        venue.genres = json.dumps(form.get('genres', venue.genres))
    
    @staticmethod
    def create_using_form_data(form):
        venue = Venue(
            name = form['name'],
            genres = json.dumps(form.getlist('genres')),
            address = form['address'],
            city = form['city'],
            state = form['state'],
            phone = form['phone'],
            facebook_link = form.get('facebook_link', ''),
            image_link = form.get('image_link', ''),
            seeking_talent = form.get('seeking_talent', False),
            seeking_description = form.get('seeking_description', ''),
            website = form.get('website', '')
        )
        return venue