"""Utility file to seed artsytrips database"""

from model import Genre, Museum, Trip, User, connect_to_db, db
from server import app


def load_genres():
    """Load genres into database."""

    print "Genres"

    Genre.query.delete()

    for row in open("seed_data/u.genre"):
        row = row.rstrip()

        genre_id, genre_code, genre_name, artist, img_url = row.split("|")

        genre = Genre(genre_code=genre_code,
        				genre_name=genre_name,
        				artist=artist,
        				img_url=img_url)

        db.session.add(genre)

    	db.session.commit()


def load_museums():
    """Load museums into database."""

    print "Museums"

    Museum.query.delete()

    for row in open("seed_data/u.museum"):
        row = row.rstrip()

        museum_id, name, genre_code, address1, address2, latitude, longitude, image = row.split("|")

        museum = Museum(name=name,
        				genre_code=genre_code,
        				address1=address1,
                        address2=address2,
                        latitude=latitude,
                        longitude=longitude,
                        image=image)
 
        db.session.add(museum)

    	db.session.commit()


def load_users():
    """Load museums into database."""

    print "Users"

    User.query.delete()

    for row in open("seed_data/fake_user_data.csv"):
        row = row.rstrip()

        name, email, password = row.split(",")

        user = User(name=name,
                    email=email,
                    password=password)

        db.session.add(user)


        db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_genres()
    load_museums()
    load_users()
