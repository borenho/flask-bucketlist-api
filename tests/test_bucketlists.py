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
            # create all tables
            db.create_all()

    def test_bucketlist_can_be_created(self):
        """Test to see that a bucketlist can be successfully created"""
        response = self.client.post('/bucketlists/', data=json.dumps(self.bucketlist), content_type='application/json')
        self.assertEqual(response.status_code, 201)    # 201 = created
        self.assertIn('Hiking', response.json.get)
