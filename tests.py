"""Tests for Artsy Trips Flask app"""

import unittest
import request_yelp
import server
from server import app
from model import db, example_data, connect_to_db
# from selenium import webdriver


class ArtsyTripsTests(unittest.TestCase):
    """Tests for the Artsy Trips site."""


    def setUp(self):
        """Code to run before every test."""
        self.client = server.app.test_client()
        app.config['TESTING'] = True


    def test_logout(self):
        """Do users who have logged out see the correct page?"""

        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn('Artsy Trips', str(result.data))

       
class ArtsyTripsTestsDatabaseWithoutSession(unittest.TestCase):
    """Flask tests that use the database."""


    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = server.app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()   


    def test_no_registration_or_login_yet(self):
        """Do users who have not registered or lovved in see the correct page?"""

        result = self.client.get('/')
        self.assertIn("<h2><center>Users' Favorited Genres</center></h2>", str(result.data))
        self.assertIn('<h1>Register</h1>', str(result.data))


class ArtsyTripsTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""


    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = server.app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


        def _mock_get_restaurant():

            return ["Paris-Cafe", "Paris-Cafe", "123 La Rue", "San Francisco, CA 94111", {'latitude': 37.123, 'longitude': -122.123}, "https://123.jpg"]
            
        request_yelp.get_restaurant = _mock_get_restaurant


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_index(self):
        """Code that tests the homepage."""

        result = self.client.get('/')
        self.assertIn("<h2><center>Users' Favorited Genres</center></h2>", str(result.data))
        self.assertIn('Artsy Trips', str(result.data))  


    def test_registration(self):
        """Do users who have registered see the correct page?"""

        registration_info = {'name': 'John' , 'email': 'john@gmail.com', 'password': '111'}

        result = self.client.post("/register", data=registration_info,
                                  follow_redirects=True)

        self.assertIn("<h2>Your Information</h2>", str(result.data))
        self.assertIn("Get directions for a trip", str(result.data))


    def test_login(self):
        """Do users who have logged in see the correct page?"""

        login_info = {'email': 'healthy@gmail.com', 'password': '111'}

        result = self.client.post("/login_process", data=login_info,
                                  follow_redirects=True)

        self.assertIn("<h2>Your Information</h2>", str(result.data))
        self.assertIn("Get directions for a trip", str(result.data))
        self.assertNotIn('<h1>Register</h1>', str(result.data))


    def test_user_profile_page(self):
        """Test user's profile page."""

        result = self.client.get('/users/1')
        self.assertIn('Healthy Child', str(result.data))


    def test_images_page(self):
        """Test page with images."""

        result = self.client.get('/images')
        self.assertIn('<img class="image" id="asa" src="https://abc/123.jpg" height="250" width="250">', str(result.data))


    def test_itinerary_page(self):
        """Test page with itinerary."""

        result = self.client.get('/itinerary/asa')
        self.assertIn('Happy Museum', str(result.data))


    def test_favorites_chart(self):
        """Test route that gives back json data."""

        result = self.client.get('/favorite_genres.json')
        self.assertIn('Expressionism', result.data)
        self.assertIn('1', result.data)


    def test_favorites_comparative_chart(self):
        """Test route that gives back json data."""

        result = self.client.get('/users/comparative_favorite_genres.json')
        self.assertIn('Impressionism', result.data)
        self.assertIn('1', result.data)   

# class TestFavoriteButtons(unittest.TestCase):
#     """Frontend test for the favorite buttons."""

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1


#     def tearDown(self):
#         self.browser.quit()


#     def test_title(self):
#         self.browser.get('http://localhost:5000/')
#         self.assertEqual(self.browser.tile, 'Home page')


#     def test_favorite(self):
#         self.browser.get('http://localhost:5000/users/1')

#         btn = self.browser.find_element_by_id('1')
#         btn.click()

#         result = self.browser.find_element_by_id('1')
#         self.assertEqual(result.getCssValue('color'), 'green')


if __name__ == "__main__":
    unittest.main()

        