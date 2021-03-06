import os
from functools import wraps
from flask import request, jsonify, make_response
import jwt
from app.database.db import Database
from app.models.model import User



def get_token():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        token = token.split(" ")[1]
    if not token:
        return make_response(jsonify({ 'status': 'failed','message': 'Token is missing!'}), 401)

    # if db.is_token_invalid(token):
    #     return make_response(jsonify({'status': 'token expired','message': 'Please login again!'}), 401)

    return token


def token_required(a):
    """
    Decorator function to ensure that end points are accessed by only authorized users provided they have a valid token
    """

    @wraps(a)
    def decorated(*args, **kwargs):
        token = get_token()
        
        try:
            database = Database()
            data = jwt.decode(token, os.environ.get('talieatalia'),)
            query = database.get_user_by_value('users', 'user_id', data['user_id'])

            if not query:
                return {"message": "User does not exist"}, 400

            current_user = User(query[0], query[1], query[2], query[3], query[4], query[5],query[5],query[6],query[7])

        except jwt.ExpiredSignatureError :
          
            return response_message('Error', 'Signature expired,please login again', 401)

        except jwt.InvalidSignatureError:
            
            return response_message('Error', 'Signature is invalid,please login again', 401)

        except jwt.DecodeError:
           
            return response_message('Error', 'please login', 401)

        return a(current_user, *args, **kwargs)

    return decorated


def response(id, username, message, token, status_code):
    """
    method to make http response for authorization token
    """
    return jsonify({
        "user_id": id,
        "username": username,
        "message": message,
        "auth_token": token

    }), status_code


def response_message(status, message, status_code):
    """
    method to handle response messages
    """
    return jsonify({
        "status": status,
        "message": message
    }), status_code
