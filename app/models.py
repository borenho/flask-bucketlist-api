"""This file holds our models - a model is a representation of a table in a database
"""
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import Column, Integer, String


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

    def __repr__(self):
        """
        Tells Python how to print objects of this class
        """
        return '<User {}>'.format(self.username)
