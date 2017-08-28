"""
This file creates a new Flask object, and returns it after it's loaded up with configuration
settings using app.config and connected to the DB using db.init_app(app)
"""
from flask import Flask, request, jsonify, abort, make_response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config.config import app_config

db = SQLAlchemy()

def create_app(configuration):
    from app.models import Bucketlist, User

    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This sets performance overhead, set to True for debugging

    db.init_app(app)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        # Get the access token from the passed header
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        access_token = auth_header.split("Bearer ")[1]
        print(access_token)
        if access_token:
            # Decode the token to get the user id
            user_id = User.decode_token(access_token)
            print(user_id)
            if not isinstance(user_id, str):
                if request.method == 'POST':
                    title = request.json.get('title')
                    print(title)
                    if title:
                        bucketlist = Bucketlist(title=title, created_by=user_id)
                        bucketlist.save()

                        response = jsonify({
                            'id': bucketlist.id,
                            'title': bucketlist.title,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': user_id
                        })
                        response.status_code = 201

                        return response
                else:
                    bucketlists = Bucketlist.get_all(user_id)
                    results = []

                    for bucketlist in bucketlists:
                        item = {
                            'id': bucketlist.id,
                            'title': bucketlist.title,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': user_id
                        }
                        results.append(item)

                    response = jsonify(results)
                    response.status_code = 200

                    return response
            else:
                # User_id not found, payload is anerror msg
                return jsonify({
                "message": "Error, could not authenticate"
            }), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def modify_bucketlist(id, **kwargs):
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if not bucketlist:
                abort(404) #Abort with a 404 not found error if buck with the id is not found

            if request.method == 'PUT':
                bucketlist.title = str(request.json.get('title', ''))
                bucketlist.save()

                response = jsonify({
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                
                response.status_code = 200

                return response

            elif request.method == 'DELETE':
                bucketlist.delete()

                # return make_response('Buck deleted', 200)

                return jsonify({
                    "message": "Bucketlist # {} deleted successfully".format(bucketlist.id)
                }), 200

            else:
                response = jsonify({
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })

                response.status_code = 200

                return response

    # Import the auth blueprint and register it
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
