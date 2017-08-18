import unittest
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """
    Class to hold tests for bucketlists
    """
    def setUp(self):
        """Holds test variables and initializes the app"""
        self.app = create_app(configuration='testing')
        self.client = self.app.test_client
        self.bucketlist = {'title': 'Hiking'}

        # Bind the app with th current context it is in
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketlist_can_be_created(self):
        """Test to see thata bucketlist can be successfully created"""
        response = self.client().post('/bucketlists', data=self.bucketlist)
