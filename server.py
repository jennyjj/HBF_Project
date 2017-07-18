from flask import Flask, request, render_template, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import os
import bcrypt

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
    return render_template("index.html")


@app.route("/favorite_genres.json")
def get_genres_favorited_by_users():
    """Return data about genres favorited."""

    trips_favorited = Trip.query.filter_by(favorited=True).all()

    museum_ids = []
    for trip in trips_favorited:
        museum_ids.append(trip.museum_id)
    
    museums = []
    for id in museum_ids:
        museum = Museum.query.filter_by(museum_id=id).first()
        museums.append(museum)

    dict_genres = {'Impressionism': 0, 'Africa, Oceania, the Americas': 0, 
                    'California Art': 0, 'Jewish Art': 0, 'Expressionism': 0, 
                    'Chinese Ink Painting': 0, 'Mixed Media': 0, 'Asian Art': 0}
    for museum in museums:
        genre_name = museum.genre.genre_name
        dict_genres[genre_name] = dict_genres.get(genre_name, 0) + 1

    genre_names = []
    counts = []
    for genre_name, count in dict_genres.items():
        genre_names.append(genre_name)
        counts.append(count) 

    data_dict = {
            "labels": genre_names,
            "datasets": [
                {
                    "data": counts,
                    "backgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#cc99ff",
                        "#0066ff",
                        "#009999",
                        "#ccff33",
                        "#990099"
                    ],
                    "hoverBackgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#cc99ff",
                        "#0066ff",
                        "#009999",
                        "#ccff33",
                        "#990099"
                    ]
                }]
        }

    return jsonify(data_dict)


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if User.query.filter_by(email=email).first():
        flash("User %s already exists." % email)
        return redirect("/")

    new_user = User(name=name, email=email, password=password_hashed)

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.user_id

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)


@app.route('/login')
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login_process', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if (bcrypt.checkpw(password.encode('utf-8'), password_hashed)) == False:
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


@app.route('/users/<int:user_id>')
def show_profile(user_id):
    """Shows profile information and trips for user."""
 
    user = User.query.filter_by(user_id=user_id).first()

    trips = Trip.query.filter_by(user_id=user_id).all()

    return render_template("user_profile.html", user=user, trips=trips)


@app.route('/users/comparative_favorite_genres.json')
def get_comparative_genres_favorited():
    """Return data about genres favorited by all users and user."""

    trips_favorited_all = Trip.query.filter_by(favorited=True).all()

    museum_ids_all = []
    for trip in trips_favorited_all:
        museum_ids_all.append(trip.museum_id)
    
    museums_all = []
    for id in museum_ids_all:
        museum = Museum.query.filter_by(museum_id=id).first()
        museums_all.append(museum)

    dict_genres_all = {'Impressionism': 0, 'Africa, Oceania, the Americas': 0, 
                    'California Art': 0, 'Jewish Art': 0, 'Expressionism': 0, 
                    'Chinese Ink Painting': 0, 'Mixed Media': 0, 'Asian Art': 0}
    for museum in museums_all:
        genre_name = museum.genre.genre_name
        dict_genres_all[genre_name] = dict_genres_all.get(genre_name, 0) + 1

    dict_genres_all = sorted(dict_genres_all.items())    
    genre_names_all = []
    counts_all = []
    for t in dict_genres_all:
        genre_names_all.append(t[0])
        counts_all.append(t[1]) 


    user_id = session['user_id']
    print user_id

    trips_favorited_user = Trip.query.filter_by(favorited=True, user_id=user_id).all()

    museum_ids_user = []
    for trip in trips_favorited_user:
        museum_ids_user = [trip.museum_id for trip in trips_favorited_user]

    museums_user = []
    for id in museum_ids_user:
        museum = Museum.query.filter_by(museum_id=id).first()
        museums_user.append(museum)

    dict_genres_user = {'Impressionism': 0, 'Africa, Oceania, the Americas': 0, 
                    'California Art': 0, 'Jewish Art': 0, 'Expressionism': 0, 
                    'Chinese Ink Painting': 0, 'Mixed Media': 0, 'Asian Art': 0}
    for museum in museums_user:
        genre_name = museum.genre.genre_name
        dict_genres_user[genre_name] = dict_genres_user.get(genre_name, 0) + 1

    dict_genres_user = sorted(dict_genres_user.items())    
    counts_user = []
    for t in dict_genres_user:
        counts_user.append(t[1])

    print dict_genres_all
    print dict_genres_user
    print counts_all
    print counts_user


    data_dict = {
            "labels": genre_names_all,
            "datasets": [
            {
                "label": "All users",
                "backgroundColor": "rgba(0, 0, 255, 0.3)",
                "borderColor": "#6600ff",
                "data": counts_all
            },
            {
                "label": "You",
                "backgroundColor":"rgba(0, 255, 0, 0.3)",
                "borderColor":"#336600",
                "data": counts_user
            }
            ]
        }

    return jsonify(data_dict)


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
    print resp

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

        db.session.add(trip)

        db.session.commit()  

    return render_template("itinerary.html", museum=museum, 
                        restaurant_name=restaurant_name, 
                        restaurant_location1=restaurant_location1, 
                        restaurant_location2=restaurant_location2, 
                        restaurant_image=restaurant_image,
                        trip=trip)


@app.route('/map/from_profile_page', methods=["POST"])
def get_map_from_profile_page():
    """Give a map and directions with starting and ending points chosen by user."""

    user_location = request.form.get("user_location")
    trip_id = request.form.get("trip_id")
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    key = os.environ['GOOGLE_API_DIRECTIONS_KEY']

    return render_template("map.html", key=key, trip=trip, user_location=user_location)


@app.route('/map/<int:trip_id>', methods=["POST"])
def get_map(trip_id):
    """Give a map and directions with starting and ending points chosen by user."""

    user_location = request.form.get("user_location")
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    key = os.environ['GOOGLE_API_DIRECTIONS_KEY']

    return render_template("map.html", key=key, trip=trip, user_location=user_location)


@app.route('/favorite.json', methods=["POST"])
def mark_favorite_status():
    """Update favorites table as to whether they have a favorited trip."""

    trip_id = request.form.get("trip_id")
    favorited = request.form.get("favorited")

    trip = Trip.query.filter_by(trip_id=trip_id).first()

    trip.favorited = favorited
    db.session.commit()

    response = { 'trip_id': trip_id, 'favorited': favorited}

    return jsonify(response)


if __name__ == "__main__":
    
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

