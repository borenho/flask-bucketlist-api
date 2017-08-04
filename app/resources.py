"""
Flask restful's Resource module giving you easy access to multiple HTTP methods
just by defining the methods on your particular resource, eg RegisterUser resource
"""
from flask_restful import Resource, reqparse
from base import add_item
from .serializer import user_serializer
from .models import User

class RegisterUser(Resource):
    """
    Resource to register a new user via the URL: /auth/register/
    """
    

    def post(self):
        """Add a user"""
        parser = reqparse.Requestparser()
        parser.add_argument('username')
        parser.add_argument('password') 
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        if username and password:
            user = User(username=username)
            user.hash_password(password)

            return add_item(
            username = username,
            item = user,
            serializer = user_serializer
        )
