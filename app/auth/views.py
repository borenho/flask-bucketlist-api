from . import auth_blueprint
from flask.views import MethodView
from flask import jsonify, request
from app.models import User

class RegistrationView(MethodView):
    """A class to register a new user"""
    def post(self):
        if request.get_json():
            user = User.query.filter_by(username=request.json.get('username')).first()

            if user:
                return jsonify({
            "message": "That username already exists, please use a different one"
            }), 202

            else:
                username = request.json.get('username')
                password = request.json.get('password')

                if not username and password:
                    return jsonify({
                    "message": "You need to pass in the username and password"
                })

                if not username:
                    return jsonify({
                "message": "The username cannot be blank, please enter a username"
                }), 400

                elif not password:
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
        else:
            return jsonify({
                "message": "You need to pass in the username and password"
            }), 401

class LoginView(MethodView):
    """
    A class based view to handle login and access to auth tokens
    """
    def post(self):
        if request.get_json():    # If something has been passed through the request
            user = User.query.filter_by(username=request.json.get('username')).first()

            if user:
                if user.verify_password(request.json.get('password')):
                    
                    access_token = user.generate_auth_token(user.id)
                    
                    if access_token:
                        return jsonify({
                            "message": "You are successfully logged in",
                            "access_token": access_token.decode()
                        }), 200

                return jsonify({
                    "message": "You entered the wrong password"
                }), 401

            username = request.json.get('username')
            password = request.json.get('password')

            if not username and password:
                return jsonify({
                "message": "You need to pass in the username and password"
            })

            if not username:
                return jsonify({
            "message": "The username cannot be blank, please enter a username"
            }), 400

            elif not password:
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
                return jsonify({
                    "message": "You are not yet registered. Please sign up for an account first"
                }), 401
        else:
            return jsonify({
                "message": "You need to pass in the username and password"
            })

    
class LogoutView(MethodView):
    """To logout a logged in user"""
    def post(self):
        auth_token = request.headers.get("Authorization").split(" ")[1]
        if auth_token:
            auth_token = None
            return jsonify({
                "message": "Logout successful"
            }), 200
        else:
            return jsonify({
                "message": "You are not logged in"
            }), 200

class ResetPasswordView(MethodView):
    """A class to allow a user to change their password"""
    def put(self):
        if not request.get_json():
            return jsonify({
            "message": "Please enter some data to proceed"
        }), 400

        data = request.get_json()
        username = data.get('username')
        new_password = data.get('password')

        if not username:
            return jsonify({
                "message": "Please enter your username"
            }), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({
                "message": "Username not found."
            }), 400

        if not new_password or new_password == "" or new_password == " ":
            return jsonify({
                "message": "The password cannot be blank, please enter a password"
                }), 400
        
        if len(new_password) < 4:
                    return jsonify({
                "message": "The password should have more than 4 characters"
                }), 400

        user.hash_password(new_password)
        user.save()

        return jsonify({
        "message": "Your password has been successfully changed"
        }), 200      

registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_password_view = ResetPasswordView.as_view('reset_password_view')

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

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func = logout_view,
    methods = ['POST']
)

auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func = reset_password_view,
    methods = ['PUT']
)
