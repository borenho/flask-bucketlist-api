"""
Blueprint organizes our app into components, eg auth compnent, bucketlist component
"""
from flask import Blueprint

# Create an insance of the auth blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views
