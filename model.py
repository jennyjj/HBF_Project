"""Models and database functions for artsytrips db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class Genre(db.Model):
    """Art genres to choose from, in order to get back an itinerary."""

    __tablename__ = "genres"

    genre_code = db.Column(db.String(100), primary_key=True, nullable=False)
    genre_name = db.Column(db.String(100), nullable=True)
    artist = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)

    # museum = db.relationship('Museum')

    def __repr__(self):
        return "<Genre genre_code=%s artist=%s img_url=%s>" % (self.genre_code, self.artist, self.img_url)


class Museum(db.Model):
    """Museum model."""

    __tablename__ = "museums"

    museum_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    genre_code = db.Column(db.String(60), db.ForeignKey('genres.genre_code'), nullable=False,)
    address = db.Column(db.String(200), nullable=False)

    genre = db.relationship('Genre', backref='museums')

    def __repr__(self):
        return "<Museum id=%s name=%s genre_code=%s address=%s>" % (self.museum_id, self.name, self.genre_code, self.address)


class Trip(db.Model):
    """Trip model."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    museum_id = db.Column(db.Integer, db.ForeignKey('museums.museum_id'), nullable=False)
    restaurant_id = db.Column(db.String(100), nullable=False)
    restaurant_name = db.Column(db.String(40), nullable=False)

    museum = db.relationship('Museum', backref='trips')
    user = db.relationship('User', backref='trips')

    def __repr__(self):
        return "<Trip id=%s museum_id=%s restaurant_id=%s>" % (self.trip_id, self.museum_id, self.restaurant_id)


class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<User id=%s name=%s email=%s>" % (self.user_id, self.name, self.email)

# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///artsytrips'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
