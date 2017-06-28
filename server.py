from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import Genre, Museum, connect_to_db
from request_yelp import get_restaurant

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = "ABC"

@app.route('/')
def go_home():
    """Goes to the homepage.  Homepage has user either login or register."""

    # Homepage welcomes user and presents login and registration options.
    return render_template("index.html")

# @app.route('/login_process')
# def login():
#   """Goes to the homepage.  Homepage has user either login or register."""

#   # Homepage welcomes user and presents login and registration options.
#   return render_template("index.html")

# @app.route('/profile', methods=["GET"])
# def show_profile():
#   """Shows profile information for user."""

#   return render_template(".html", )

@app.route('/images')
def show_images():
    """Shows user images to choose from, to establish his/her art genre."""

    genres = Genre.query.all()

    return render_template("art.html", genres=genres)

@app.route('/itinerary/<genre_code>', methods=["GET"])
def show_itinerary(genre_code):
    """Give an itinerary including trips to a museum and eatery."""

    museum = Museum.query.filter_by(genre_code=genre_code).first()

    location = museum.address

    restaurant_info = get_restaurant(location)

    return render_template("itinerary.html", museum=museum, restaurant_info=restaurant_info)


if __name__ == "__main__":
    
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

