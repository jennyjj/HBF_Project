from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import Image

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = "ABC"

@app.route('/')
def go_home():
	"""Goes to the homepage.  Homepage has user either login or register."""

	# Homepage welcomes user and presents login and registration options.
	return render_template("index.html")

@app.route('/login_process')
def go_home():
	"""Goes to the homepage.  Homepage has user either login or register."""

	# Homepage welcomes user and presents login and registration options.
	return render_template("index.html")

@app.route('/profile', methods=["GET"])
def show_profile():
	"""Shows profile information for user."""

	return render_template(".html", )

@app.route('/images')
def show_profile():
	"""Shows user images to choose from, to establish his/her art genre."""

	return render_template("art.html")

@app.route('/itinerary', methods=["POST"])
def show_itinerary():
	"""Give an itinerary including trips to a museum and eatery."""

	return render_template(".html", )


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")