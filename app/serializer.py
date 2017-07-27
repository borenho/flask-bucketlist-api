"""
    This file defines how to represent/serialize the models
    Used by marshmallow
"""
# Customize the db fields to a formatting we want
from flask_restful import fields

user_serializer = {
    "id": fields.Integer,
    "username": fields.String
}
