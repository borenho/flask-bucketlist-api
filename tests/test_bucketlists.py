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

    def test_api_can_get_bucketlist_by_id(self):
        """Test api can get a single bucketlist, belonging to a single user"""
        self.register_sample_user()
        registered_user = self.login_sample_user()
        access_token = json.loads(registered_user.data.decode())['access_token']

        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer " + access_token),
            data = json.dumps(self.bucketlist), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        results = json.loads(response.data.decode())
        bucketlist = self.client.get(
            '/bucketlists/{}'.format(results['id']),
            headers = dict(Authorization="Bearer {}".format(access_token))
        )
        # Assert that the bucketlist is returned, given its id
        self.assertEqual(bucketlist.status_code, 200)
        self.assertIn('Hiking', str(bucketlist.data))

    def test_bucketlist_can_be_edited(self):
        """Test api can edit a bucketlist, PUT request"""
        self.register_sample_user()
        login = self.login_sample_user()
        access_token = json.loads(login.data.decode())['access_token']

        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer " + access_token),
            data = json.dumps({"title": "All work and no play makes Jack a dull boy."}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        results = json.loads(response.data.decode())

        # Make a put request to edit the bucketlist
        response = self.client.put(
            '/bucketlists/{}'.format(results['id']),
            headers = dict(Authorization="Bearer " + access_token),
            data = json.dumps({"title": "Work and play makes Jack a smart boy."}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # Pick the edited bucketlist to see if it's actually edited
        results = self.client.get(
            '/bucketlists/{}'.format(results['id']),
            headers = dict(Authorization="Bearer {}".format(access_token)))

        self.assertIn('smart boy', str(results.data))

    def test_bucketlist_can_be_deleted(self):
        """Test bucketlist can be deleted, by DELETE request"""
        self.register_sample_user()
        login = self.login_sample_user()
        access_token = json.loads(login.data.decode())['access_token']

        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer " + access_token),
            data = json.dumps({"title": "Pete is cooling hot maandazi. Sorry, I meant burgers"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        results = json.loads(response.data.decode())

        # Delete the bucketlist we just created
        response = self.client.delete(
            '/bucketlists/{}'.format(results['id']),
            headers = dict(Authorization="Bearer {}".format(access_token)))
        
        self.assertEqual(response.status_code, 200)

        # Test to see if it can find the deleted buck, it should return a 404
        results = self.client.get(
            '/bucketlists/{}'.format(results['id']),
            headers = dict(Authorization="Bearer {}".format(access_token)))
        self.assertEqual(results.status_code, 404)
