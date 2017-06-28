"""Utility file to seed artsytrips database"""

from model import Genre, Museum, connect_to_db, db
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

        museum_id, name, genre_code, address = row.split("|")

        museum = Museum(name=name,
        				genre_code=genre_code,
        				address=address)
 
        db.session.add(museum)

    	db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_genres()
    load_museums()
    
