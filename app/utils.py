# This module contains the functions that will validate users data
# some imports


import os
import re
from functools import wraps
import jwt
from flask import jsonify, request, abort, make_response
from werkzeug.security import generate_password_hash
from datetime import datetime
import jwt

# local imports
from app.admin.models import AuthToken
from app.admin.models import UserModel
from app.admin.db import select_data_from_db

key = os.getenv("SECRET_KEY")


def check_password(password, confirmed_password):
  
    '''
     Lets check if our passoword meets the requirements
    '''
    # check to confirm the password is of required length
    if len(password) < 8 or len(password) > 20:
        abort(make_response(jsonify(status=400, error="Password should not be less than 8 characters or exceed 20"), 400))

    # check if password contains at least an alphabet(a-z)
    if not re.search("[a-z]", password):
        abort(make_response(jsonify(status=400, error="Password should contain a letter between a-z"), 400))

    # check if password contains at least an upper case letter
    if not re.search("[A-Z]", password):
        abort(make_response(jsonify(status=400, error="Password should contain a capital letter"), 400))

    # check if password contains at least a number(0-9)
    if not re.search("[0-9]", password):
        abort(make_response(jsonify(status=400, error="Password should contain a number(0-9)"), 400))

    # Checks if passwords provided by the users match
    if password != confirmed_password:
        abort(make_response(jsonify(status=400, error="Your passwords don't match!"), 400))

    # hash the password with sha256 algorithm.
    hashed_password = generate_password_hash(password, method='sha256')

    return hashed_password


# validate email
def validate_email(email):
    """
    Is the email valid , is it already used?
    """
    try:
        user, domain = str(email).split("@")
        if not re.match("^[A-Za-z]*$", user):
            abort(make_response(jsonify({
                "status": 400, "Error":  "Email is Invalid"}), 400))
    except ValueError:
        abort(make_response(jsonify(
            status=400,
            error="Email is Invalid"), 400))
    if not user or not domain:
        abort(make_response(jsonify(error="Email is Invalid"), 400))

    # Check that domain is valid
    try:
        domain_1, domain_2 = domain.split(".")
        if not re.match("^[A-Za-z]*$", domain_1):
            abort(make_response(jsonify({
                "status": 400, "Error":  "Email is Invalid"}), 400))
        if not re.match("^[A-Za-z]*$", domain_2):
            abort(make_response(jsonify({
                "status": 400, "Error":  "Email is Invalid"}), 400))
    except ValueError:
        abort(make_response(jsonify(
            status=400,
            error="Email is Invalid"), 400))
    if not domain_1 or not domain_2:
        abort(make_response(jsonify(
            status=400,
            error="Email is Invalid"), 400))

    return email


# wrap our function and check for the access-token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': "Token is missing"}), 401

        blacklisted = AuthToken.check_if_token_blacklisted(token)
        if blacklisted:
            abort(make_response(jsonify({
                'message': 'Please login again to continue'}), 401))

        try:
            data = jwt.decode(token, key)
            query = """
            SELECT username FROM users
            WHERE users.username = '{}'""".format(data['username'])

            specific_user = select_data_from_db(query)

        except:
            return jsonify({'message': 'Token is expired or invalid'}), 401

        return f(specific_user, *args, **kwargs)
    return decorated


#lets decode our token back
def decode_token():
    token = request.headers['x-access-token']
    try:
        username = jwt.decode(token, key)
    except:
        return jsonify({"message": "Token is expired or invalid"}), 401

    return username

#lests verify if the user is an admin or not
"""
def verify_if_user_is_admin(username):
        admin = None
        for user in USERS_LEN:
            if username == 'blairtheadmin':
                user.is_admin = True
                admin = True
            admin = False
        return admin
        """


def check_duplication(params, table_name):
    for key, value in params.items():
        query = """
        SELECT {} from {} WHERE {}.{} = '{}'
        """.format(key, table_name, table_name, key, value)
        duplicated = select_data_from_db(query)
        if duplicated:
            abort(make_response(jsonify(
                status=400,
                error="Error. '{}' '{}' \
is already in use".format(key, value)), 400))


# check if the user is actually an admin
def check_if_user_is_admin():
    username = decode_token()
    if username['username'] != "admin":
        return False
    return True


# lets check for any whitespace that may exists and return true if found
def check_for_whitespace(data):
    """
    Check for whitespace only in input data
    """
    for keys, value in data.items():
        if keys != 'tags':
            if not value.strip():
                abort(make_response(jsonify({
                    'status': 400,
                    'error':'{} field cannot be left blank'.format(keys)}), 400))
        if keys == 'tags':
            for tags in data['tags']:
                if not tags.strip():
                    abort(make_response(jsonify({
                        'status': 400,
                        'error':'tags field cannot be left blank'}), 400))
    return True


# check for other validations
"""
def check_if_string(data):
    if not re.match("^[A-Za-z]*$", data['firstname']):
        abort(make_response(jsonify({
            "status": 400,
            "Error":  "Make sure you only use letters in your firstname"}), 400))

    if not re.match("^[A-Za-z]*$", data['lastname']):
        abort(make_response(jsonify({
            "status": 400, "Error":
            "Make sure you only use letters in your lastname"}), 400))

    if not re.match("^[A-Za-z]*$", data['username']):
        abort(make_response(jsonify({
            "status": 400,
            "Error":  "Make sure you only use letters in your username"}), 400))
"""


def check_if_string(data):
    for key, value in data.items():
        if key in ['firstname', 'lastname', 'username']:
            if not value.isalpha():
                abort(make_response(jsonify({
                    "status": 400,
                    "Error":  "Make sure you only use letters in your {}".format(key)}), 400))


def check_phone_number(phone):
    if not re.match('^[0-9]*$', phone):
        abort(make_response(jsonify({
            "status": 400,
            "Error":  "Phone number should be integers only"}), 400))

    if len(phone) < 10 or len(phone) > 10:
        abort(make_response(jsonify({
            "status": 400,
            "Error":  "Phone number should be 10 digits."}), 400))


def check_date(date):
    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/([12][0-9]{3})$", date):
        abort(make_response(jsonify({
            "status": 400, "Error":  "Invalid date format. Should be DD/MM/YYYY"}), 400))

    date_format = "%d/%m/%Y"
    strpdate = datetime.strptime(date, date_format)
    now = datetime.now()

    if strpdate < now:
        abort(make_response(jsonify({
            "status": 400, "Error":  "Date should be in the future"}), 400))

    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    format_date = date[0:2]+ " " + months[int(date[3:5]) -1] + " " + date[6:]
    return format_date


# has the user already responded "yes" to the meetup
def check_if_rsvp_already_exists(meetup_id, user_id):
    query = """
    SELECT rsvp_id FROM rsvps
    WHERE rsvps.meetup_id = '{}' AND rsvps.user_id = '{}'
    AND rsvps.rsvp = '{}'
    """.format(meetup_id, user_id, 'yes')

    rsvp = select_data_from_db(query)
    return rsvp