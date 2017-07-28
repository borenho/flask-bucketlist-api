import unittest, json
from ..app import create_app, db

class AuthTestCase(unittest.TestCase):
    """
    Test cases for the auth blueprint
    """
    def setUp(self):
        """ Set the test variables """
        self.app = create_app(configuration='testing')
        self.client = self.app.test_client
        # Set some user data in json format
        self.user_data = {
            'username': 'kaka',
            'password': 'hard-to-guess-1090'
        }

        with self.app.app_context():
            # Drop all existing tables and re-create them
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        """Test user reg works"""
        response = self.client.post('auth/register', data=self.user_data)
        # Return the results in json format
        result = json.loads(response.data.decode)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], "Account successfully created")
        