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
    from app.models import Bucketlist

    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This sets performance overhead, set to True for debugging

    db.init_app(app)

    # Import the auth blueprint and register it
    # from .auth import auth_blueprint
    # app.register_blueprint(auth_blueprint)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        if request.method == 'POST':
            title = request.json.get('title')
            if title:
                bucketlist = Bucketlist(title=title)
                bucketlist.save()

                response = jsonify({
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201

                return response
        else:
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                item = {
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(item)

            response = jsonify(results)
            response.status_code = 200

            return response

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

    return app
