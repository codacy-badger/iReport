from flask import jsonify, request, Blueprint
from datetime import datetime
import psycopg2
from app.database.db import Database
from flask import current_app as app
from flask_mail import Message, Mail
import os
import config
from app.auth.decorator import response_message, token_required
from validate_email import validate_email
from flasgger import swag_from

flags = Blueprint('redflags', __name__)

db = Database()
mail = Mail(app)



def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# POST redflags
@flags.route('/api/v1/redflags', methods=['POST'])
@token_required
def add_redflag(current_user):
    if not request.content_type == 'application/json':
        return jsonify({"failed": 'Content-type must be application/json'}), 415
    request_data = request.get_json()

    if not request.content_type == 'application/json':
        return jsonify({"failed": 'Content-type must be application/json'}), 415
    request_data = request.get_json()

    try:

        db.insert_into_redflag(current_user.user_id,
                               request_data['type'],
                               request_data['media'],
                               request_data['location()'],
                               request_data['description'],
                               request_data['createdby'],
                               request_data['get_timestamp()']
                               )

        if not validate_email(request_data['user_email']):
            return jsonify({"message": "User email is invalid"}), 400

        if len(str(request_data['description'])) < 10:
            return jsonify({"message": "Your redflag description should be atleast more than 50 characters"}), 400

        if not isinstance(request_data['description'], str):
            return jsonify({"message": "Description should be string values"}), 400

        if not isinstance(request_data['location'], str):
            return jsonify({"message": "location should be string values"}), 400

        if not isinstance(request_data['type'], str):
            return jsonify({"message": "redflag_type should be string values"}), 400

        if not isinstance(request_data['createdby'], int):
            return jsonify({"message": "createdby should be string values"}), 400

    except KeyError as item:
        return response_message('Failed', str(item) + 'is missing', 400)

    except psycopg2.IntegrityError:
        return response_message('message', 'something went wrong', 403)
    return jsonify({'status': '200', 'data': '', 'id': '', 'message': 'redflag created successfully'})

@flags.route('/api/v1/location', methods=['POST'])
@token_required
def location(self):
        """
        add location of incidence
        """
        try:
            locate = requests.get(
                "https://www.mapquestapi.com/geocoding/v1/address?key=" + self.talieatalia + "&inFormat=kvp&outFormat=json&location= ")
            data = locate.json()
            results = data['results'][0]
            locations = results['locations']
            latlng = locations[0].get('latLng')
            return latlng
        except :
            return {"lat": -0.90629, "lng": 27.19168}


def update(data):
    if 'location' in data:
        return True
    return False

# PATCH REDFLAG LOCATION
@flags.route('/api/v1/redflag/<int:id>/Location', methods=['PUT'])
@token_required
def update_location(current_user, id):
    """
    update the redflag location
    """
    if not db.user_id(current_user.user_id):
        return response_message('Unauthorized', 'no access', 401)
    request_data = request.get_json()
    try:
        if not isinstance(request_data['location()'], str):
            return response_message('error', 'location should be string', 400)

        if not db.get_redflag_by_id('redflags', 'redflag_id', id):
            return jsonify({'message': 'redflag not available'}), 404

        if update(request_data):
            db.change_location(request_data['location()'], id)
            our_user = db.get_user_by_value(
                'users', 'user_id', db.get_redflag_owner_id(id))
            sendemail(our_user[5], 'Redflag location Update',
                      'Greetings to you' + our_user[4] + '\nYour redflag location has been updated to ' + db.get_location(id))
            return jsonify({'message': 'location updated successfully', 'Location': db.get_location(id)}), 200

# GET redflags
@flags.route('/api/v1/redflags')
@token_required
def get_redflags(current_user):
    if not db.isAdmin(current_user.user_id):
        return response_message('unauthorized operation', 'Only admin users can view all_flags orders', 401)
    all_flags = db.get_redflags()
    if all_flags:
        redflag = []
        for flag in all_flags:
            redflag_dict = {
                'flag_id': flag[0],
                'user_id': flag[1],
                'description': flag[2],
                'created_by': flag[3],
                'media': flag[4],
                'location': flag[5],
                'status': flag[6],
                'createdOn': datetime.datetime.utcnow()
            }
            redflag.append(redflag_dict)
        return jsonify({"redflags": redflag}), 200
    return jsonify({'message': 'No redflag created'}), 404

# GET REDFLAG BY ID


@flags.route('/api/v1/redflags/<int:id>')
@token_required
def get_a_redflag(current_user, id):
    """
    return redflag details for a specific redflag
    """
    if not db.isAdmin(current_user.user_id):
        if str(current_user.user_id) != str(id):
            return response_message('unauthorized operation', 'You dont have permissions to access', 401)

    if db.get_redflag_by_id('redflags', 'redflag_id', id) is None:
        return jsonify({"message": "redflag post not found"}), 404
    return jsonify({"status": "200", "data": "redflags"})


# DELETE redflag
@flags.route('/api/v1/redflags/<int:id>/delete', methods=['DELETE'])
@token_required
def delete_redflag(current_user, id):
    '''
    deletes a specific redflag posted by id
    '''
    if db.get_redflag_by_id('redflags', 'redflag_id', id) is None:
        return jsonify({"message": "redflag not found"}), 404

    if db.is_redflag_resolved(id):
        return jsonify({"message": "Redflag has already been resolved"}), 403

    if not db.is_redflag_owner(id, current_user.user_id):
        return jsonify({"message": "Not authorized"}), 401

    return jsonify({"message": "redflag deleted successfully", "redflag_id": db.delete_redflag(id)[0], "new_redflag_status": db.delete_redflag(id)[6]}), 200

# admin access to the red flags


@flags.route('/api/v1/users/<int:id>/redflags', methods=['GET'])
@token_required
def get_user_redflag(current_user, id):
    if not db.isAdmin(current_user.user_id):
        if current_user.user_id != id:
            return response_message('unauthorized operation', 'You do not have access to here ', 401)

    if not db.get_user_by_value('users', 'user_id', id) is None:

        try:
            flag = Database().get_redflags()
            redflag_list = []

            for flag in db.get_user_redflags(id):
                redflag_dict = {
                    'flag_id': flag[0],
                    'user_id': flag[1],
                    'description': flag[2],
                    'created_by': flag[3],
                    'media': flag[4],
                    'location': flag[5],
                    'createdOn': datetime.datetime.utcnow()
                }
                redflag_list.append(redflag_dict)
            return jsonify({"redflags": redflag_list}), 200

        except:
            return jsonify({"message": 'User does not exist'}), 404

    else:
        return jsonify({"message": 'User does not exist'}), 404


@flags.route('/api/v1/redflags/<int:id>/status', methods=['PUT'])
@token_required
def change_redflag_status(current_user, id):
    if not db.isAdmin(current_user.user_id):
        return response_message('Unauthorized', 'You dont have access here', 401)
    request_data = request.get_json()
    try:

        if not isinstance(request_data['status'], str):
            return response_message('error', 'status should be string value', 400)
        status = ['received', 'rejected',
                  'under_investigation', 'resolved', 'on-going']

        if not db.get_redflag_by_id('redflags', 'redflag_id', id):
            return jsonify({'message': 'redflag not found'}), 404
        if not request_data['status'] in status:
            return jsonify(
                {'message': "invalid status,redflags can be received,rejected,under_investigation,resolved,on-going"}), 400

        db.change_status(request_data['status'], id)
        our_user = db.get_user_by_value(
            'users', 'user_id', db.get_redflag_owner_id(id))
        sendemail(our_user[5], 'redflag Status Update',
                  'Greetings to you' + our_user[4] + '\nYour redflags status has changed to ' + request_data['status'])
        return jsonify({'message': 'redflag status updated successfully', 'new_status': request_data['status']}), 200
    except:
        return response_message('error', 'status not attached', 400)


def sendemail(email, subject, body):
    '''
    send an email to a user
    '''
    try:
        message = Message(subject,
                          sender="updates@iReporter.com",
                          recipients=[email])
        message.body = body
        mail.send(message)
        return 'mail sent'
    except:
        pass
