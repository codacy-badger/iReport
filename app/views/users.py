import jwt
import re
import datetime 
from flask import Blueprint,Flask, jsonify, json, request
from app.auth.decorator import response_message, token_required,get_token
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from validate_email import validate_email
from app.database.db import Database
from app.model.models import User
# from app.views. import sendemail
import os
from flask_cors import CORS

user = Blueprint('user1', __name__)

db = Database()
CORS(user)

# user registration 

@user.route('/api/v1/register', methods=['POST'])
def register():
    """
        User creates an account
        User sign up details are added to the data base
        """
    if request.content_type != 'application/json':
        return response_message(
            'Bad request', 'Content-type must be json type', 400)
    request_data = request.get_json()

    try:
        if not request_data:
            return jsonify({"message": "Request not made"}), 400

        firstname = request_data['firstname']
        lastname = request_data['lastname']
        othernames = request_data['othername']
        phonenumber = request_data['phonenumber']
        email = request_data['email']
        username = request_data['username']
        str(username).replace(" ", "")

        if not firstname or not lastname or not othernames:
            return response_message('Missing', 'Name is required', 400)

        phone_number = str(request_data['phone_number'])
        if len(phone_number) < 10:
            return response_message('Invalid', 'phone number should be atleast 10 characters', 400)

        if not re.match("[0-9]", phone_number):
            return response_message('Invalid', 'phone number should only contain numbers', 400)

        if not isinstance(username, str):
            return response_message('Invalid', 'username should be of type string', 400)

        if len(username) < 3:
            return response_message('Invalid', 'username should be atleast 3 characters', 400)

        if not username:
            return response_message('Missing', 'Username required', 400)

        if not validate_email(email):
            return response_message('Error', 'Missing or wrong email format', 400)

        if not len(request_data['password']) > 5:
            return response_message('Failed', 'password must be atleast 6-8 characters', 400)

        if db.get_user_by_value('users', 'email', email):
            return response_message('Failed', 'User with email ' + email + ' already exists', 409)

        if db.get_user_by_value('users', 'username', username):
            return response_message('Failed', username + ' is taken', 409)

        password = generate_password_hash(request_data['password'])
        db.insert_into_user(firstname, lastname, othernames, username, email, phone_number, password)
        sendemail(email, 'Welcome to iReporter Journalism platform',
            'Greeting to you  ' + username + ',\n Thank you for joining this platform which is a self participating platform to stop corruption in our country\nTo do so please use the platform to report, record an audio, video, image about corupt minds. No need to be afraid\nRemember comrruption starts with you if you keep silent\n Lets join hands to fight it\nRegards iReporter')
        return response_message('Success', 'Account successfully created', 201)
    except KeyError as item:
        return jsonify({'Error': str(item) + ' is missing'}), 400


# user Login
@user.route('/api/v1/login', methods=['POST'])
def login_user():
    """
    User logins with correct credentials
    token is generated and given to a user
    """
    try:
        if request.content_type != 'application/json':
            return response_message(
                'Bad request', 'Content-type must be in json', 400)
        request_data = request.get_json()

        if not request_data:
            return jsonify({"Failed": "Request can't be empty"}), 400

        email = request_data['email']
        if not validate_email(email):
            return response_message('Failed', 'email is invalid', 400)

        password = request_data['password']
        db_user = db.get_user_by_value('users', 'email', email)
        if not db_user:
            return response_message('Failed', 'email or password is invalid', 401)

        new_user = User(
            db_user[0], db_user[1], db_user[2], db_user[3],
            db_user[4], db_user[6])
        if not check_password_hash(new_user.password, password):
            return response_message('Failed', 'email or password is invalid', 400)
        payload = {

            'exp': datetime.datetime.utcnow() +
                   datetime.timedelta(days=0, hours=23),
            'user_id': new_user.user_id,
            'email': new_user.email,
            'isAdmin': new_user.isAdmin
        }

        token = jwt.encode(
            payload,
            'talieatalia',
            algorithm='HS256'
        )

        if token:
            return jsonify({"message": "logged in successfully ", "auth_token": token.decode('UTF-8'),'user_id':new_user.user_id,'isADmin':new_user.isADmin}), 200

    except Exception as er:
        return response_message('Failed', 'email or password is invalid', 400)


@user.route('/api/v1/users', methods=['GET'])
@token_required
def get_users(current_user):
    if not db.isADmin(current_user.user_id):
        return response_message('unauthorized operation', 'Only admin users can view all users', 401)
    users = Database().get_users()
    user_list = []
    for user in users:                        
        user_dict = {
            "user_id": user[0],
            "fullname": user[1],
            "username": user[2],
            "email": user[3],
            "phone_number": user[5],
            "isADmin": user[6],
            "joined": user[7]
        }
    user_list.append(user_dict)

    if len(user_list) == 0:
        return jsonify({"message":"no registered user"})
        
    return jsonify({"users": user_list}), 200

# admin access to the red flags

@user.route('/api/v2/users/<int:id>/parcels', methods=['GET'])
@token_required
# @swag_from('../doc/user_parcels.yml')
def get_user_redflag(current_user, id):
    if not db.is_admin(current_user.user_id):
        if current_user.user_id != id:
            return response_message('unauthorized operation', 'You do not have permissions to access that', 401)

    if not db.get_user_by_value('users', 'user_id', id) is None:
       
        try:
            redflag_list = []

            for redflag in db.get_user_redflag(id):
                redflag_dict = {
                    'flag_id':flag_id,
                    'location': location,
                    'type': type,
                    'description': description,
                    'image': image,
                    'video' : video,
                    str(dt.utcnow()) : created_on,
                    'created_by' : created_by
                }
                redflag_list.append(redflag_dict)
            return jsonify({"redflags": redflag_list}), 200
            
        except IndexError as e:
            return jsonify({"message": 'User does not exist'}), 404

    else:
        return jsonify({"message": 'User does not exist'}), 404

