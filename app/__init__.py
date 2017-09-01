"""
This file creates a new Flask object, and returns it after it's loaded up with configuration
settings using app.config and connected to the DB using db.init_app(app)
"""
from flask import Flask, request, jsonify, abort, make_response, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config.config import app_config

db = SQLAlchemy()

def create_app(configuration):
    from app.models import Bucketlist, User, BucketlistItem

    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This sets performance overhead, set to True for debugging

    db.init_app(app)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        # Get the access token from the passed header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split("Bearer ")[1]
            if access_token:
                # Decode the token to get the user id
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str):
                    if request.method == 'POST':
                        title = request.json.get('title')
                        if title:
                            bucketlists = Bucketlist.get_all(user_id)
                            if bucketlists:
                                for bucketlist in bucketlists:
                                    if title == bucketlist.title:
                                        return jsonify({
                                        "message": "The title should be unique, use a different name"
                                    })

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
                    else:    # If GET
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

                        if not results:
                            return jsonify({
                            "message": "Hey, you don't have bucketlist yet, please create one"
                        }), 404

                        return response
                else:
                    # User_id not found, payload is an error msg
                    return jsonify({
                    "message": "Error, could not authenticate. Please login first"
                }), 401
            else:
                    # No access token
                    return jsonify({
                    "message": "Error, access token not found, you need to login first"
                }), 401
        else:   # No auth_header
            return jsonify({
                    "message": "Error, access token not found, you need to login first"
                }), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def modify_bucketlist(id, **kwargs):
        # Get the access token from the passed header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split("Bearer ")[1]
        if access_token:
            # Decode the token to get the user id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
                if not bucketlist:
                        return jsonify({
                        "message": "Sorry, you don't have a bucketlist with that id"
                    }), 404

                if request.method == 'PUT':
                    title = request.json.get('title')
                    bucketlists = Bucketlist.get_all(user_id)
                    if bucketlists:
                        for bucket in bucketlists:
                            if title == bucket.title:
                                return jsonify({
                                "message": "The title should be unique, use a different name"
                            })
                            else:
                                bucketlist.title = title
                                bucketlist.save()

                                response = jsonify({
                                    'id': bucketlist.id,
                                    'title': bucketlist.title,
                                    'date_created': bucketlist.date_created,
                                    'date_modified': bucketlist.date_modified,
                                    'created_by': user_id
                                }), 200

                                return response

                elif request.method == 'DELETE':
                    bucketlist.delete()

                    return jsonify({
                        "message": "Bucketlist # {} deleted successfully".format(bucketlist.id)
                    }), 200

                else:    # GET
                    response = jsonify({
                        'id': bucketlist.id,
                        'title': bucketlist.title,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': user_id
                    })

                    response.status_code = 200

                    return response
            else:
                # User_id not found, payload is an error msg
                return jsonify({
                "message": "Error, could not authenticate. Please login first"
            }), 401

    
    @app.route('/bucketlists/<int:bucketlist_id>/items', methods=['GET', 'POST'])
    def bucketlist_items(bucketlist_id, **kwargs):
        # Get the access token from the passed header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split("Bearer ")[1]
        if access_token:
            # Decode the token to get the user id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=bucketlist_id, created_by=user_id).first()
                if not bucketlist:
                        return jsonify({
                        "message": "Sorry, you don't have a bucketlist with that id"
                    }), 404

                if request.method == 'POST':
                    title = request.json.get('title')
                    if title:
                        bucketlist_item = BucketlistItem(title=title, bucketlist_id=bucketlist_id)
                        bucketlist_item.save()

                        response = jsonify({
                            'id': bucketlist_item.id,
                            'title': bucketlist_item.title,
                            'date_created': bucketlist_item.date_created,
                            'date_modified': bucketlist_item.date_modified,
                            'bucketlist_id': bucketlist_id 
                        })
                        response.status_code = 201

                        return response
                else:    # If GET
                    bucketlist_items = BucketlistItem.get_all(bucketlist_id)
                    results = []

                    for bucketlist_item in bucketlist_items:
                        item = {
                            'id': bucketlist_item.id,
                            'title': bucketlist_item.title,
                            'date_created': bucketlist_item.date_created,
                            'date_modified': bucketlist_item.date_modified,
                            'bucketlist_id': bucketlist_id
                        }
                        results.append(item)

                    response = jsonify(results)
                    response.status_code = 200

                    if not results:
                        return jsonify({
                        "message": "Hey, you don't have a bucketlist item here yet, please create one"
                    }), 404

                    return response
            else:
                # User_id not found, payload is an error msg
                return jsonify({
                "message": "Error, could not authenticate. Please login first"
            }), 401
        else:
                # No access token
                return jsonify({
                "message": "Error, access token not found, you need to login first"
            }), 401

        
    @app.route('/bucketlists/<bucketlist_id>/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
    def modify_bucketlist_item(bucketlist_id, item_id, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split("Bearer ")[1]
        if access_token:
            # Decode the token to get the user id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=bucketlist_id, created_by=user_id).first()
                if not bucketlist:
                        return jsonify({
                        "message": "Sorry, you don't have a bucketlist with that id"
                    }), 404

                bucketlist_item = BucketlistItem.query.filter_by(bucketlist_id=bucketlist_id, id=item_id).first()
                if not bucketlist_item:
                    return jsonify({
                    "message": "Sorry, this bucketlist item does not exist"
                }), 401

                if request.method == 'PUT':
                    bucketlist_item.title = request.json.get('title')
                    bucketlist_item.save()

                    response = jsonify({
                        'id': bucketlist_item.id,
                        'title': bucketlist_item.title,
                        'date_created': bucketlist_item.date_created,
                        'date_modified': bucketlist_item.date_modified,
                        'bucketlist_id': bucketlist_id
                    }), 200

                    return response

                elif request.method == 'DELETE':
                    bucketlist_item.delete()

                    # return make_response('Buck deleted', 200)

                    return jsonify({
                        "message": "Bucketlist Item # {} deleted successfully".format(bucketlist_item.id)
                    }), 200

                else:    # GET
                    response = jsonify({
                        'id': bucketlist_item.id,
                        'title': bucketlist_item.title,
                        'date_created': bucketlist_item.date_created,
                        'date_modified': bucketlist_item.date_modified,
                        'bucketlist_id': bucketlist_id
                    })

                    response.status_code = 200

                    return response
            else:
                # User_id not found, payload is an error msg
                return jsonify({
                "message": "Error, could not authenticate. Please login first"
            }), 401
    # Import the auth blueprint and register it
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
