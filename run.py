"""This file define an entry point to start our app
"""
import os
from app import create_app
from flask_restful import Api

configuration = os.getenv('APP_SETTINGS')    # configuration = 'development'
app = create_app(configuration)


if __name__ == '__main__':
    app.run()
 