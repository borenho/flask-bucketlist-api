"""
This file defines models for which we create a database and
define r/ships between them
"""
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import Column, Integer, String, DateTime                       
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    def generate_auth_token(self, time_to_expire=3600):
        """
        Generates a token for authentication that expires after 1 hr
        """
        serializer = Serializer(os.environ.get('SECRET_KEY'), expires_in=time_to_expire)
        return serializer.dumps({'id': self.id})    # Dumps serializes to a JSON-encoded string, eg {"name": "Monty", "email": "monty@python.org"}

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
