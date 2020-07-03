from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from .errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

@token_auth.verify_token
def verify_token(token):
    # g.current_user = User.check_token_validity(token) if token else None
    # return g.current_user is not None
    if token:
        g.current_user = User.check_token_validity(token)
    else:
        g.current_user = None
    if g.current_user is not None:
        return g.current_user

@token_auth.error_handler
def token_auth_error():
    return error_response(401)