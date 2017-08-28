import unittest
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """
    Class to hold tests for bucketlists
    """
    def setUp(self):
        """Holds test variables and initializes the app"""
        self.app = create_app(configuration='testing')
        self.client = self.app.test_client()
        self.bucketlist = {'title': 'Hiking'}

        # Bind the app with the current context it is in
        with self.app.app_context():
            # Drop all existing tables and re-create them
            db.session.close()
            db.drop_all()
            db.create_all()

    # Create helper functions to register and sign in a test user who can crud bucketlists
    def register_sample_user(self, username="kaka", password="kaka10"):
        test_user_data = {
            'username': username,
            'password': password
        }

        return self.client.post('/auth/register', data=json.dumps(test_user_data), content_type='application/json')

    def login_sample_user(self, username="kaka", password="kaka10"):
        test_user_data = {
            'username': username,
            'password': password
        }

        return self.client.post('/auth/login', data=json.dumps(test_user_data), content_type='application/json')

    def test_bucketlist_can_be_created(self):
        """Test to see that a bucketlist can be successfully created"""
        self.register_sample_user()
        result = self.login_sample_user()
        # Get the auth token and add it to the authorization header
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer {}".format(access_token)),
            data=json.dumps(self.bucketlist), content_type='application/json')

        self.assertEqual(response.status_code, 201)    # 201 = created
        self.assertIn('Hiking', response.data.decode())

    def test_can_get_a_users_bucketlists(self):
        self.register_sample_user()
        result = self.login_sample_user()
        # Get the auth token and add it to the authorization header
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer {}".format(access_token)),
            data=json.dumps(self.bucketlist), content_type='application/json')

        self.assertEqual(response.status_code, 201)    # 201 = created
        # GET all bucketlists that belong to the test user
        response = self.client.get(
            '/bucketlists/',
            headers = dict(Authorization="Bearer {}".format(access_token))
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hiking', response.data.decode())

    # def test_api_can_get_bucketlist_by_id(self):
    #     pass
