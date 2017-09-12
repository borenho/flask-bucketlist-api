import unittest
import json
from app import create_app, db

class BucketlistItemTestCase(unittest.TestCase):
    """
    Class to hold tests for bucketlist items
    """
    def setUp(self):
        """Holds test variables and initializes the app"""
        self.app = create_app(configuration='testing')
        self.client = self.app.test_client()
        self.bucketlist_item = {'title': 'Go visit grandma'}

        # Bind the app with the current context it is in
        with self.app.app_context():
            # Drop all existing tables and re-create them
            db.session.close()
            db.drop_all()
            db.create_all()

    # Create helper functions to register and sign in a test user who can crud bucketlists and bucketlist items
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
        

    def test_bucketlist_item_can_be_created(self):
        """Test to see that a bucketlist item can be successfully created"""
        self.register_sample_user()
        result = self.login_sample_user()
        # Get the auth token and add it to the authorization header
        access_token = json.loads(result.data.decode())['access_token']

        # Create the parent bucketlist
        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer {}".format(access_token)),
            data=json.dumps({"title": "Riding"}), content_type='application/json')

        bucketlist_id = json.loads(response.data.decode())['created_by']

        # Create the bucketlist item
        response = self.client.post(
            '/bucketlists/{}/items'.format(bucketlist_id),
            headers = dict(Authorization="Bearer {}".format(access_token)),
            data=json.dumps(self.bucketlist_item), content_type='application/json')

        self.assertEqual(response.status_code, 201)    # 201 = created
        self.assertIn('grandma', response.data.decode())

    def test_api_can_get_bucketlist_items(self):
        """Test to see that a bucketlist item can be successfully fetched from db"""
        self.register_sample_user()
        result = self.login_sample_user()
        # Get the auth token and add it to the authorization header
        access_token = json.loads(result.data.decode())['access_token']

        # Create the parent bucketlist
        response = self.client.post(
            '/bucketlists/',
            headers = dict(Authorization="Bearer {}".format(access_token)),
            data=json.dumps({"title": "Riding"}), content_type='application/json')

        bucketlist_id = json.loads(response.data.decode())['created_by']

        # Create the bucketlist item
        response = self.client.post(
            '/bucketlists/{}/items'.format(bucketlist_id),
            headers = dict(Authorization="Bearer {}".format(access_token)),
            data=json.dumps(self.bucketlist_item), content_type='application/json')

        item_id =json.loads(response.data.decode())['id']

        results = self.client.get(
            '/bucketlists/' + str(bucketlist_id) + '/items/' + str(item_id),
            headers = dict(Authorization="Bearer {}".format(access_token))
        )
        self.assertEqual(results.status_code, 200)
        self.assertIn('grandma', response.data.decode())
