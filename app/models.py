"""
This file defines models for which we create a database and
define r/ships between them
"""
import os
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta                     
import jwt


class User(db.Model):
    """
    Represents the class user table in the db
    """
    __tablename__ = 'users'    # Table name should always be plural

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', cascade='all, delete-orphan')

    def hash_password(self, password):
        """
        Hashes the password and stores it
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Checks if stored hashed password matches hash of the newly entered password
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, id):
        """
        Generates a token for authentication
        """
        # Create a payload/claim
        payload = {
            "iss": id,    # iss = issuer of token
            "exp": datetime.utcnow() + timedelta(minutes=60)    # iat = issued at time
        }
        jwt_string = jwt.encode(payload, os.getenv('SECRET'), algorithm='HS256')
        
        return jwt_string

    @staticmethod
    def decode_token(token):
        """Decode the auth token from the authorization header"""
        if jwt.ExpiredSignatureError:
            return jsonify({
            "message": "Expired token, please login to get a new token"
        })

        if jwt.InvalidTokenError:
            return jsonify({
            "message": "Invalid token, please register or login to get a new token"
        })

        decoded_token = jwt.decode(token, os.getenv('SECRET'), algorithm='HS256')
        
        return decoded_token
        
    def save(self):
        """Method to save user"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """
        Tells Python how to print objects of this class
        """
        return '<User {}>'.format(self.username)


class Bucketlist(db.Model):
    """ 
    To create the table Bucketlists in the db
    """
    __tablename__ = 'bucketlists'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    date_created = Column(DateTime, default = db.func.current_timestamp())
    date_modified = Column(DateTime,
        default = db.func.current_timestamp(),
        onupdate = db.func.current_timestamp()
    )
    created_by = Column(Integer, db.ForeignKey(User.id))

    def __init__(self, title, created_by):
        """Initialize the table with a title"""
        self.title = title
        self.created_by = created_by

    def save(self):
        """Method to save to the bucketlists table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Method to delete a bucketlist"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """Method to get all bucketlists of this table"""
        return Bucketlist.query.filter_by(created_by=user_id)

    def __repr__(self):
        """Tells Python how to print objects of this class"""
        return "<Bucketlist : {}>".format(self.title)
