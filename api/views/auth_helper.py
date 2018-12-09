# import os
# import sy/s
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from functools import wraps
import datetime
import jwt
from flask import request, jsonify
from models.user_model import User,users_table

secret_key = "klgwso7dbnc37hgv8oiawb/we9h7_hywg8"


def encode_token(userId):
    token = jwt.encode({'userId': User.userId,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5)},
                       secret_key)
    return token


def decode_token(token):
    define = jwt.decode(token, secret_key, algorithms=['HS256'])
    return define


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers['token']
            try:
                decoded = decode_token(token)
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "token expired"}), 401
            except jwt.InvalidSignatureError:
                return jsonify({"message": "Signature verification failed"}), 401
            except jwt.InvalidTokeneError:
                return jsonify({"message": "Invalid Token verification failed"}), 401
        except KeyError:
            return jsonify({"message": "Missing token"}), 401
        return wrapper


def get_current_user():
    """Fetches current user details from database"""
    token = request.headers['token']
    decoded_token = decode_token(token)
    try:
        user_id = decode_token["userId"]
        for user_obj in users_table:
            if user_obj.userId == user_id:
                return {"username":user_obj.userName,"email":user_obj.email,"isAdmin":user_obj.isAdmin}
    except KeyError:
        return jsonify({"message": "user_id not in token"}), 401


def admin_required(func):
    """This decorator limits access to the routes to admin user only"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        isAdmin = get_current_user()['isAdmin']
        if isAdmin:
            return func(*args, **kwargs)
        return jsonify({"messsage": "Only admin can access this route"}), 401

    return wrapper


def non_admin_required(func):
    """This decorator limits access to the routes to non admin user only"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        isAdmin = get_current_user()['isAdmin']
        if not isAdmin:
            return jsonify({"messsage": "Only Non admin can access this route"}), 401
        return func(*args, **kwargs)

    return wrapper
