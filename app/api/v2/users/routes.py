import os
import datetime
import jwt
from flask import request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

from app.admin.models import UserModel, AuthToken
from app.api.v2 import path_2
from app.utils import validate_email, check_password, check_if_user_is_admin
from app.admin import db
from app import utils
from app.utils import token_required


KEY = os.getenv('SECRET_KEY')


# tests for user signup 
@path_2.route("/auth/signup", methods=['POST'])
def user_sign_up():

    try:
        data = request.get_json()  # to minimize redundancy
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        email = data['email']
        password = data['password']
        confirmPass = data['confirm_password']
        phone = data['phoneNumber']
      
    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     'error': "Should be firstname, lastname, username, email, phoneNumber, password and confirm_password"}), 400))

    # check_password(password, confirm_pass)
    # email = validate_email(email)

    utils.check_for_whitespace(data)
    utils.check_if_string(data)
    utils.check_phone_number(phone)
    utils.check_password(password, confirmPass)
    email = utils.validate_email(email)

    utils.check_duplication({"username": username}, "users")
    utils.check_duplication({"email": email}, "users")

    user = UserModel(firstname=firstname,
                     lastname=lastname,
                     phone=phone,
                     username=username,
                     email=email,
                     password=password)

    # call the save_user method from the models
    user.save_user()
    return jsonify({"status": 201, "data": "User Registered Successfully!"}), 201


# login route
@path_2.route("/auth/login", methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            'error': "Should be username & password"}), 400))

    utils.check_for_whitespace(data)

    try:
        user = UserModel.get_user_by_username(username)
        if not user:
            return jsonify({"status": 400,
                            "data": "The username or passsword is incorrect"}), 400

        user_id = user[0][0]
        username = user[0][1]
        email = user[0][2]
        hashed_password = user[0][3]

        password = UserModel.check_if_password_in_db(hashed_password, password)
        if not password:
            abort(make_response(jsonify({'status': 400,
                                         'error': "The paswsord is wrong"}), 400))

        token = jwt.encode({"username": username}, KEY, algorithm='HS256')
        return jsonify({"status": 200, "token": token.decode('UTF-8'),
                        "message": "Logged in successfully"}), 200

    except psycopg2.DatabaseError as error:
        abort(make_response(jsonify(message="Server error : {}".format(error)), 500))\

# invalidate user token on logout
@path_2.route("auth/logout", methods=["POST"])
@token_required
def logout(specific_user):  #logs out a specific user from thr system
    token = request.headers['x-access-token']

    blacklist_token = AuthToken(token=token)
    blacklist_token.blacklist_token()

    return jsonify({'status': 200,
                    'data': 'Logged out successfully'}), 200
        