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
    username = Column(String(50))
    email = Column(String(50), unique=True, index=True)
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
            "exp": datetime.utcnow() + timedelta(minutes=1200)    # iat = issued at time (token expires after 20hrs)
        }
        jwt_string = jwt.encode(payload, os.getenv('SECRET'), algorithm='HS256')
        
        return jwt_string

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, os.getenv('SECRET'))
            return payload['iss']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return jsonify({
                "message": "Expired token. Please login to get a new token"
                }), 403
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return jsonify({
                "message": "Invalid token. Please register or login"
                }), 403
        
    def save(self):
        """Method to save user"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """
        Tells Python how to print objects of this class
        """
        return '<User {}>'.format(self.email)


class Bucketlist(db.Model):
    """ 
    To create the table Bucketlists in the db
    """
    __tablename__ = 'bucketlists'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, index=True, nullable=False)
    date_created = Column(DateTime, default = db.func.current_timestamp())
    date_modified = Column(DateTime,
        default = db.func.current_timestamp(),
        onupdate = db.func.current_timestamp()
    )
    created_by = Column(Integer, db.ForeignKey(User.id))
    bucketlist_items = db.relationship('BucketlistItem', order_by='BucketlistItem.id', cascade='all, delete-orphan')

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

    @staticmethod
    def title_exists(title):
        """Checks if a bucketlist with the passed name already exists in the db"""
        return Bucketlist.query.filter_by(title=title).first()

    def __repr__(self):
        """Tells Python how to print objects of this class"""
        return "<Bucketlist : {}>".format(self.title)


class BucketlistItem(db.Model):
    """ 
    To create the table BucketlistItems in the db
    """
    __tablename__ = 'bucketlist_items'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, index=True, nullable=False)
    date_created = Column(DateTime, default = db.func.current_timestamp())
    date_modified = Column(DateTime,
        default = db.func.current_timestamp(),
        onupdate = db.func.current_timestamp()
    )
    bucketlist_id = Column(Integer, db.ForeignKey(Bucketlist.id))

    def __init__(self, title, bucketlist_id):
        """Initialize the table with a title and its parent's id"""
        self.title = title
        self.bucketlist_id = bucketlist_id

    def save(self):
        """Method to save to the bucketlists table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Method to delete a bucketlist"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all(bucketlist_id):
        """Method to get all bucketlists of this table"""
        return BucketlistItem.query.filter_by(bucketlist_id=bucketlist_id)

    @staticmethod
    def title_exists(title):
        """Checks if an item with the passed name already exists in the db"""
        return BucketlistItem.query.filter_by(title=title).first()

    def __repr__(self):
        """Tells Python how to print objects of this class"""
        return "<Bucketlist Item : {}>".format(self.title)
