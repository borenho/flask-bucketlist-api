"""
Flask restful's Resource module giving you easy access to multiple HTTP methods
just by defining the methods on your particular resource, eg RegisterUser resource
"""
from flask_restful import Resource, reqparse
from serializer import user_serializer
from models import User

class RegisterUser(Resource):
    """
    Resource to register a new user via the URL: /auth/register/
    """

    def post(self):
        """Add a user"""
        
