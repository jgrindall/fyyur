from ..extensions import db
import json

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
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

    
