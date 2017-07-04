from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import os

from model import Genre, Museum, Trip, User, connect_to_db, db
from request_yelp import get_restaurant

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = "ABC"


@app.route('/')
def go_home():
    """Goes to the homepage.  Homepage has user either login or register."""
    # if session.has_key("user_id"):
    #         return redirect("/users/%s" % session['user_id'])

    # # Homepage welcomes user and presents login and registration options.
    return render_template("index.html")



@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.user_id

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)


@app.route('/login')
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)

@app.route('/logout')
def logout():
    """Log out."""
    if session.has_key('user_id'):
        del session["user_id"]
        flash("Logged Out.")
    return redirect("/")

@app.route('/users/<user_id>')
def show_profile(user_id):
    """Shows profile information and trips for user."""
 
    user = User.query.filter_by(user_id=user_id).first()

    trips = Trip.query.filter_by(user_id=user_id).all()

    return render_template("user_profile.html", user=user, trips=trips)


@app.route('/images')
def show_images():
    """Shows user images to choose from, to establish his/her art genre."""

    genres = Genre.query.all()

    return render_template("art.html", genres=genres)


@app.route('/itinerary/<genre_code>', methods=["GET"])
def show_itinerary(genre_code):
    """Give an itinerary including trips to a museum and eatery."""

    museum = Museum.query.filter_by(genre_code=genre_code).first()

    location = museum.address1 + museum.address2

    resp = get_restaurant(location)

    if resp == None:
        return "An error has occurred."   
    restaurant_id, restaurant_name, restaurant_location1, restaurant_location2, restaurant_coordinates, restaurant_image = resp

    restaurant_latitude = float(restaurant_coordinates['latitude'])  
    restaurant_longitude = float(restaurant_coordinates['longitude']) 

    if None in list(resp):
        return "An error has occurred"

    if 'user_id' in session:
        user_id = session["user_id"]

        trip = Trip(user_id=user_id,
                museum_id=museum.museum_id,
                restaurant_id=restaurant_id,
                restaurant_name=restaurant_name,
                restaurant_longitude=restaurant_longitude,
                restaurant_latitude=restaurant_latitude)  

        user_id = session.get("user_id")

        db.session.add(trip)

        db.session.commit()  

    return render_template("itinerary.html", museum=museum, 
                        restaurant_name=restaurant_name, 
                        restaurant_location1=restaurant_location1, 
                        restaurant_location2=restaurant_location2, 
                        restaurant_image=restaurant_image,
                        trip=trip)


@app.route('/map/<trip_id>')
def get_map(trip_id):
    """Give a map marking the chosen museum and restaurant for the user."""

    user_location = request.form.get("user_location")

    trip = Trip.query.filter_by(trip_id=trip_id).first()
    print trip
    key = os.environ['GOOGLE_API_KEY']

    return render_template("map.html", key=key, trip=trip, user_location=user_location)



if __name__ == "__main__":
    
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

