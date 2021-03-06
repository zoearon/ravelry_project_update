import unittest
from selenium import webdriver

from freezegun import freeze_time
from server import app
from model import db, example_data, connect_to_db
import api
from seed import sync_projects


class ServerTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("projects", result.data)

    def test_no_user_yet(self):
        result = self.client.get("/")
        self.assertIn("Login", result.data)
        self.assertNotIn("Logout", result.data)

    def test_login_form(self):
        result = self.client.get("/login")
        self.assertIn("Login", result.data)
        self.assertIn("username", result.data)
        self.assertNotIn("abc", result.data)

    def test_user_no_user(self):
        """Test user page works. """

        result = self.client.get("/user", follow_redirects=True)
        self.assertIn("Login", result.data)
        self.assertIn("password", result.data)
        self.assertNotIn("abc", result.data)

    def test_project_no_user(self):
        """ Test that the project page redirects to login if no current user """

        result = self.client.get("/projects", follow_redirects=True)
        self.assertIn("Login", result.data)
        self.assertIn("password", result.data)
        self.assertNotIn("abc", result.data)


@freeze_time("2017-10-31")
class ServerTestsDatabase(unittest.TestCase):
    """ Flask tests that use database"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        def f_date():
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 31)

    def tearDown(self):
        """Do at end of every test."""

        db.drop_all()
        db.session.close()

    def test_login(self):
        """ Test login page works. """
        result = self.client.post("/login",
                                  data={'username': "abc", 'password': "123"},
                                  follow_redirects=True)
        self.assertIn("abc", result.data)
        self.assertIn("Logout", result.data)
        self.assertIn("Successful", result.data)
        self.assertNotIn("password", result.data)

    def test_login_fail(self):
        """ Test login page works for wrong user info. """
        result = self.client.post("/login",
                                  data={'username': "123", 'password': "joe"},
                                  follow_redirects=True)
        self.assertIn("username", result.data)
        self.assertNotIn("Successful", result.data)
        self.assertIn("password", result.data)

@freeze_time("2017-10-31")
class ServerTestsDatabaseSession(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        def f_date():
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 31)

        def _mock_post_add_image(project, user, up_image):
            pass

        api.post_add_image = _mock_post_add_image

        def _mock_sync_update(user):
            return "test update"

        sync_projects = _mock_sync_update

        def _mock_post_project_api_update(project, up_notes,
                                          up_status, up_progress, user):
            pass

        api.post_project_api_update = _mock_post_project_api_update

        # add a session
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.drop_all()
        db.session.close()

    def test_user(self):
        """Test user page works. """

        result = self.client.get("/user")
        self.assertIn("abc", result.data)
        self.assertIn("Logout", result.data)
        self.assertNotIn("password", result.data)

    def test_logout(self):
        """ Test logout route """

        result = self.client.get("/logout", follow_redirects=True)

        self.assertIn("Login", result.data)
        self.assertIn("username", result.data)
        self.assertNotIn("abc", result.data)

    def test_projects(self):
        """Test projects page."""

        result = self.client.get("/projects")
        self.assertIn("Need Updates", result.data)
        self.assertNotIn("basic", result.data)

    def test_project_details(self):
        """Test project details page. """

        result = self.client.get("/projects/1")
        self.assertIn("Logout", result.data)
        self.assertIn("knit hat", result.data)
        self.assertIn("Test", result.data)
        self.assertNotIn("username", result.data)
        self.assertIn("https://i.vimeocdn.com/portrait/58832_300x300",
                      result.data)

    def test_project_details_post(self):
        """Test project details page. """

        result = self.client.post("/projects/1",
                                  data={'notes': "FINISHED",
                                        'img-url': 'https://cdn0.iconfinder.com/data/icons/the-essential/30/check_ok-512.png',
                                        'status': '2'},
                                  follow_redirects=True)
        self.assertIn("Logout", result.data)
        self.assertIn("knit hat", result.data)
        self.assertIn("Test", result.data)
        self.assertIn('FINISHED', result.data)
        self.assertNotIn("username", result.data)
        self.assertIn("https://i.vimeocdn.com/portrait/58832_300x300",
                      result.data)
        self.assertIn("https://cdn0.iconfinder.com/data/icons/the-essential/30/check_ok-512.png",
                      result.data)
        self.assertIn("Successful", result.data)

    def test_user_update(self):
        """ Test when a user updates their profile information """

        pass
        '/user/update'

    def test_user_sync(self):
        """ Test mock of user sync function """

        result = self.client.get("/sync")
        self.assertIn("test update", result)

# class SeliniumTest(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome("../chromedriver")

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/')
#         self.assertEqual(self.browser.title, 'Projects')

#     def test_login(self):
#         self.browser.get('http://localhost:5000/login')
#         self.assertEqual(self.browser.title, 'Login')


if __name__ == "__main__":
    unittest.main()
