"""
This file defines models for which we create a database and
define r/ships between them
"""
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import Column, Integer, String, Datetime                                    
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    """
    Represents the class user table in the db
    """
    __tablename__ = 'users'    # Table name should always be plural

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)


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
        return serializer.dumps({'id': self.user_id})    # Dumps serializes to a JSON-encoded string, eg {"name": "Monty", "email": "monty@python.org"}

    def __repr__(self):
        """
        Tells Python how to print objects of this class
        """
        return '<User {}>'.format(self.username)


class Bucketlist(db.model):
    """ 
    To create the table Bucketlists in the db
    """
    __tablename__ = 'bucketlists'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    date_created = Column(Datetime, default = db.func.current_timetamp())
    date_modified = Column(Datetime,
        default = db.func.current_timetamp(),
        onupdate = db.func.current_timetamp()
    )

    def __init__(self, title):
        """Initialize the table with a title"""
        self.title = title

    def save(self):
        """Method to save to the bucketlists table"""
        db.session.add(self)
        db.session.commit()

    def delete_table(self):
        """Method to delete the bucketlists table"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Method to get all bucketlists of this table"""
        return Bucketlist.query.all()

    def __repr__(self):
        """Tells Python how to print objects of this class"""
        return "<Bucketlist : {}>".format(self.title)
