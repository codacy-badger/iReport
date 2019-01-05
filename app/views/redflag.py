from flask import jsonify, request, Blueprint
from datetime import datetime
import psycopg2
from app.database.db import Database
from flask import current_app as app
from flask_mail import Message, Mail
import os
from app.auth.decorator import response_message, token_required
from validate_email import validate_email
from flasgger import swag_from

flags = Blueprint('redflags', __name__)
db = Database()

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# GET redflags

@flags.route('/api/v1/redflags')
@token_required
@swag_from('../doc/get_all_redflags.yml')
def get_redflags(current_user):
    if not db.isAdmin(current_user.user_id):
        return response_message('unauthorized operation', 'Only admin users can view all_flags orders', 401)
    all_flags = db.get_all_redflags()
    if all_flags:
        redflag = []
        for flag in all_flags:
            redflag_dict = {
                "flag_id": flag_id ,
                "user_id": user_id ,
                "description": description ,
                "user_email": user_email ,
                "status": status ,
                "location": location ,
                "createdby": createdby, 
                "createdOn": get_timestamp()
            }
            redflag.append(redflag_dict)
        return jsonify({"redflags": redflag}), 200
    return jsonify({'message': 'No redflag created'}), 404


# def get_redflags(current_user):
# # GET redflags/id
#     pass

@flags.route('/api/v1/redflags/<int:id>')
@token_required
@swag_from('../doc/get_a_redflag.yml')
def get_a_redflag(current_user, id):
    """
    return redflag details for a specific redflag
    """
    if not db.isAdmin(current_user.user_id):
        if str(current_user.user_id) != str(id):
            return response_message('unauthorized operation', 'You dont have permissions to access', 401)
    if db.get_redflag_by_value('redflags', 'redflag_id', id) is None:
        return jsonify({"message": "redflag post not found"}), 404
    results = db.get_redflag_by_value('redflags', 'redflag_id', id)
    redflag_dict = {
        "redflag_id": results[0],
        "user_id": results[1],
    }

@flags.route('/api/v1/redflags')
@token_required
def get_redflags(current_user):
# GET redflags/id
    redflag_dict{
        "flag_id": flag_id ,
        "user_id": user_id ,
        "description": description ,
        "user_email": user_email ,
        "status": status ,
        "location": location ,
        "createdby": createdby, 
        "createdOn": get_timestamp(),
        "last_modified": last_modified
        }
    return jsonify(redflag_dict), 200
        


# POST redflags
@flags.route('/api/v1/redflags', methods=['POST'])
@token_required
@swag_from('../doc/new_redflag.yml')
def add_redflag(current_user):
    if not request.content_type == 'application/json':
        return jsonify({"failed": 'Content-type must be application/json'}), 415
    request_data = request.get_json()
    helper = Helper()
    try:
        if not validate_email(request_data['user_email']):
            return jsonify({"message": "User email is invalid"}), 400

        if len(str(request_data['user_phone_number'])) < 10:
            return jsonify({"message": "user Phone number should be atleast 10 characters"}), 400

        if len(str(request_data['redflag_description'])) < 10:
            return jsonify({"message": "Your redflag description should be atleast more than 50 characters"}), 400

        if not isinstance(request_data['redflag_description'], str):
            return jsonify({"message": "Description should be string values"}), 400

        if not isinstance(request_data['location'], str):
            return jsonify({"message": "location should be string values"}), 400

        if not isinstance(request_data['redflag_type'], str):
            return jsonify({"message": "redflag_type should be string values"}), 400

        if not isinstance(request_data['createdOn'], int):
            return jsonify({"message": "createdOn should be integer values"}), 400

        if not isinstance(request_data['createdby'], int):
            return jsonify({"message": "createdby should be string values"}), 400


    except KeyError as item:
        return response_message('Failed', str(item) + 'is missing', 400)


    try:

        db.insert_into_redflag(request_data['redflag_type'],
                               request_data['location'],
                               request_data['redflag_description'],
                               current_user.user_id,
                               db.get_user_email(current_user.user_id),
                               request_data['createdby'],
                               request_data['get_timestamp()']
                              )
    except psycopg2.IntegrityError:
        return response_message('message', 'something went wrong', 403)
    return response_message('success', 'redflag created successfully', 201)


# PUT /redflags/<redflagId>/cancel
@flags.route('/api/v1/redflags/<int:id>/cancel', methods=['PUT'])
@swag_from('../doc/cancel_redflagl.yml')
@token_required

def delete_redflag_request(current_user, id):
    '''
    deletes a specific request given its identifier
    '''
    if db.get_redflag_by_value('redflags', 'redflag_id', id) is None:
        return jsonify({"message": "redflag not found"}), 404

    if db.is_redflag_resloved(id):
        return jsonify({"message": "Redflag has already been resolved"}), 403

    if not db.is_redflag_owner(id, current_user.user_id):
        return jsonify({"message": "Not authorized"}), 401

    return jsonify({"message": "redflag deleted successfully", "redflag_id": db.delete_redflag(id)[0], "new_redflag_status": db.delete_redflag(id)[6]}), 200


@flags.route('/api/v1/redflags/<int:id>/presentLocation', methods=['PUT'])
@token_required
@swag_from('../doc/change_present_locationn.yml')
def change_present_location(current_user, id):
    if not db.isAdmin(current_user.user_id):
        return response_message('Unauthorized', 'Not enough access previleges', 401)
    request_data = request.get_json()
    try:
        if not isinstance(request_data['current_location'], str):
            return response_message('error', 'current location should be string value', 400)
        if not db.get_redflag_by_value('redflags', 'redflag_id', id):
            return jsonify({'message': 'order not found'}), 404
        if is_should_update(request_data):
            db.change_present_location(request_data['current_location'], id)
            our_user = db.get_user_by_value('users', 'user_id', db.get_parce_owner_id(id))
            sendemail(our_user[3], 'Order Update',
                      'Hello there ' + our_user[1] + '\nYour redflags location is now ' + db.get_current_location(id))
            return jsonify({'message': 'current location updated successfully',
                            'Present Location': db.get_current_location(id)}), 200
        else:
            return jsonify({'message': 'bad request object, current location missing'}), 400

    except KeyError as identifier:
        return jsonify({'message': str(identifier) + 'is missing'})


@flags.route('/api/v1/redflags/<int:id>/status', methods=['PUT'])
@token_required
@swag_from('../doc/status.yml')
def change_order_status(current_user, id):
    if not db.is_admin(current_user.user_id):
        return response_message('Unauthorized', 'Not enough access privileges', 401)
    request_data = request.get_json()
    try:

        if not isinstance(request_data['status'], str):
            return response_message('error', 'status should be string value', 400)
        status = ['pickup_started', 'rejected', 'in_transit', 'cancelled', 'delivered']

        if not db.get_redflag_by_value('redflags', 'redflag_id', id):
            return jsonify({'message': 'order not found'}), 404
        if not request_data['status'] in status:
            return jsonify(
                {
                    'message': "invalid status,redflags can be cancelled,delivered,in_transit,rejected,pickup_started"}), 400

        db.change_status(request_data['status'], id)
        our_user = db.get_user_by_value('users', 'user_id', db.get_parce_owner_id(id))
        sendemail(our_user[3], 'Order Status Update',
                  'Hello there ' + our_user[1] + '\nYour redflags status ' + request_data['status'])
        return jsonify({'message': 'order status updated successfully', 'new_status': request_data['status']}), 200
    except KeyError as e:
        return response_message('error', 'status is missing', 400)


@flags.route('/api/v1/redflags/<int:id>/destination', methods=['PUT'])
@token_required
@swag_from('../doc/changedestination.yml')
def change_destination(current_user, id):
    rdata = request.get_json()
    if not "redflag_type" in rdata:
        return jsonify({'message': 'Please add a new destination address'}), 400

    newdest = rdata['redflag_type']
    if db.get_redflag_by_value('redflags', 'redflag_id', id) is None:
        return jsonify({"message": "redflag delivery request not found"}), 404
    # CHECK SAME DESTINATION ADDRESSES
    if str(db.get_redflag_type(id)).lower() == str(newdest).lower():
        return response_message('Forbidden', 'Not authorised to perform operation', 401)

    if not db.is_order_delivered(id):
        if db.is_redflag_owner(id, current_user.user_id):
            our_user = db.get_user_by_value('users', 'user_id', 100)
            sendemail(our_user[3], 'Destination Update',
                      'Hello there \n New Destination Update for ' + current_user.username + '\nNew Destination is  ' + db.change_destination(
                          newdest, id))

            return jsonify({'message': 'destination updated successfully',
                            'new_destination': db.change_destination(newdest, id)}), 200
        else:
            return response_message('Forbidden', 'Not authorised to perform operation', 401)

    else:
        return jsonify({'message': 'order already delivered cant update'}), 403


def not_validresponse():
    return jsonify({"error": 'Bad Request object,expected data is missing'}), 400


def is_should_update(data):
    if 'current_location' in data:
        return True
    return False


def sendemail(email, subject, body):
    '''
    send an email to a user
    '''
    app.config.update(
        DEBUG=True,
        # EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=os.environ.get('trulysEmail'),
        MAIL_PASSWORD=os.environ.get('trulysPass')

    )
    mail = Mail(app)
    try:
        message = Message(subject,
                          sender="updates@iReporter.com",
                          recipients=[email])
        message.body = body
        mail.send(message)
        return 'mail sent'
    except Exception as identifier:
        pass
