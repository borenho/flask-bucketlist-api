from . import auth_blueprint
from flask.views import MethodView
from flask import jsonify, request
from app.models import User

class RegistrationView(MethodView):
    """A class to register a new user"""
    def post(self):
        user = User.query.filter_by(username=request.json.get('username')).first()

        if user:
            return jsonify({
        "message": "That username already exists, please use a different one"
        }), 400

        else:
            username = request.json.get('username')
            password = request.json.get('password')

            if not username or username == "":
                return jsonify({
            "message": "The username cannot be blank, please enter a username"
            }), 400

            elif not password or password == "":
                return jsonify({
            "message": "The password cannot be blank, please enter a password"
            }), 400

            elif len(username) < 4:
                return jsonify({
            "message": "The username should have more than 4 characters"
            }), 400

            elif len(password) < 4:
                return jsonify({
            "message": "The password should have more than 4 characters"
            }), 400

            else:
                user = User(username=username)
                user.hash_password(password)
                user.save()

                return jsonify({
            "message": "Hey {}, you have been successfully registered".format(username)
            }), 201

class LoginView(MethodView):
    """
    A class based view to handle login and access to auth tokens
    """
    def post(self):
        user = User.query.filter_by(username=request.json.get('username')).first()

        if user:
            if user.verify_password(request.json.get('password')):
                
                access_token = user.generate_auth_token(user.id)
                
                if access_token:
                    return jsonify({
                        "message": "You are successfully logged in",
                        "access token": access_token.decode()
                    }), 200

            return jsonify({
                "message": "You entered the wrong password"
            }), 401

        return jsonify({
            "message": "You are not yet registered. Please sign up for an account first"
        }), 401

registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func = registration_view,
    methods = ['POST']
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func = login_view,
    methods = ['POST']
)
