from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Optional, Regexp, AnyOf, ValidationError
from .consts import states, genres

genres_allowed = [genre[0] for genre in genres]
states_allowed = [state[0] for state in states]

phone_error = "Phone number can include digits and -, and can start with a '+' for international numbers"
phone_validator = Regexp(r'^\+?\d[\d-]+$',message=phone_error)

state_error = "Invalid state."
state_validator = AnyOf(states_allowed, message=state_error)

def genres_validator(form, field):
    selected_genres = field.data
    if not set(selected_genres).issubset(genres_allowed):
        raise ValidationError(f"Genre mismatch")
    


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )



class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), state_validator],
        choices=states
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), phone_validator]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), genres_validator],
        choices=genres
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    website = StringField(
        'website', validators=[Optional(), URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), state_validator],
        choices=states
    )
    phone = StringField(
        'phone', validators=[DataRequired(), phone_validator]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), genres_validator],
        choices=genres
     )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
     )

    website = StringField(
        'website', validators=[Optional(), URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
        'seeking_description'
     )

