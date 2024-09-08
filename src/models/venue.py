from ..extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(8), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(32))
    image_link = db.Column(db.String(512))
    facebook_link = db.Column(db.String(512))
    genres = db.Column(ARRAY(db.String), nullable=False)

    seeking_talent = db.Column(db.Boolean, default=False, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    website = db.Column(db.String(512), nullable=True)

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
            "genres":self.genres
        }
    
    @staticmethod
    def edit_using_form_data(venue, form):
        venue.name = form.data['name']
        venue.city = form.data['city']
        venue.state = form.data['state']
        venue.address = form.data['address']
        venue.phone = form.data['phone']
        venue.image_link = form.data['image_link']
        venue.facebook_link = form.data['facebook_link']
        venue.seeking_talent = form.data['seeking_talent']
        venue.seeking_description = form.data['seeking_description']
        venue.website = form.data['website']
        venue.genres = form.data["genres"]
    
    @staticmethod
    def create_using_form_data(form):

        print("1", form.data, flush=True)

        venue = Venue(
            name = form.data["name"],
            genres = form.data["genres"],
            address = form.data["address"],
            city = form.data["city"],
            state = form.data["state"],
            phone = form.data["phone"],
            facebook_link = form.data["facebook_link"],
            image_link = form.data["image_link"],
            seeking_talent = form.data["seeking_talent"],
            seeking_description = form.data["seeking_description"],
            website = form.data["website"]
        )
        return venue