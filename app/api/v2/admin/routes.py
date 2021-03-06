"""The meetup routes"""
import json
from datetime import datetime
from flask import jsonify, request, make_response, abort

from app.admin.models import MeetupModel
from app.api.v2 import path_2
from app.utils import check_if_user_is_admin, token_required
from app.admin.models import UserModel, UserRsvp, UserVote
from app import utils


@path_2.route("/meetups", methods=['POST'])
@token_required
def admin_create_meetup(specific_user):
    """
    POST a meetup : POST admin/meetups
    """
    try:
        topic = request.get_json()['topic']
        happenningon = request.get_json()['happenningon']
        location = request.get_json()['location']
        images = request.get_json()['images']
        tags = request.get_json()['tags']

# return error message with the corresponding status code defined in the kenyetechbytes.com
    except:
        return jsonify({'status': 400,
                        'error': 'Check the json keys you have used very well'}), 400

    if not topic:
        return jsonify({'status': 400, 'error': 'Provide the topic field'}), 400
    if not happenningon:
        return jsonify({'status': 400, 'error': 'provide the meetup date'}), 400

    if not location:
        return jsonify({'status': 400, 'error': 'provide the location'}), 400

    if not tags:
        return jsonify({'status': 400, 'error': 'provide the tags'}), 400

    admin = check_if_user_is_admin()
    if not admin:
        return jsonify({'status': 401, 'error': "You are not allowed to perfom this function"}), 401
  
    # lets do validations
    try:
        data = request.get_json()
        topic = data['topic']
        happenningon = data['happenningon']
        location = data['location']
        images = data['images']
        tags = data['tags']

    except KeyError:
        return jsonify({
            'status': 400,
            'error': 'Should be topic, happenningon, location, images and tags'}), 400

    utils.check_for_whitespace(data)
    utils.check_if_string(data)

    if not tags:
        abort(make_response(jsonify({
            'status': 400,
            'error': 'tags field is required'}), 400))

    happenningon = utils.check_date(happenningon)
    # check if a meetup already exists
    meetup_id = MeetupModel.check_if_meetup_already_exists(location, happenningon)
    if meetup_id:
        abort(make_response(jsonify({
            'status': 409,
            'error': 'Meetup already exists. Choose another location or date'
        }), 409))

    # let admin add tag array to the database
    tags = json.dumps(data['tags'])

    meetup = MeetupModel(
        topic=topic,
        happenningon=happenningon,
        location=location,
        images=images,
        tags=tags
    )
    meetup.save_meetup_record()

    # return a jsonify string with an OK status
    return jsonify({"status": 201,
                    "data": [{"topic": topic,
                              "location": location,
                              "happenningon": happenningon,
                              # "images": images,
                              "tags": tags}]}), 201


# user gets a specific meetup record
@path_2.route("/meetups/<int:meetup_id>", methods=["GET"])
def get_specific_meetup(meetup_id):
    meetup = MeetupModel.get_specific_meetup(meetup_id)
    if meetup:
        meetup = meetup[0]  # assign it index 0 =1 
        return jsonify({"status": 200, "data": {'meetupId': meetup['meetup_id'],
                                                'topic': meetup['topic'],
                                                'happenningon': meetup['happenningon'],
                                                'location': meetup['meetup_location']}}), 200
    return jsonify({"status": 404, "error": "Meetup with id {} not found".format(meetup_id)}), 404


# User get all upcoming meetup records endpoint
@path_2.route("/meetups/upcoming", methods=["GET"])
def get_all_upcoming_meetups():
    meetups = MeetupModel.get_all_upcoming_meetups()

    if meetups:
        return jsonify({"status": 200, "data": meetups}), 200
    return jsonify({
        "status": 404,
        "error": "No upcoming meetups available."
    }), 404


# user respond to a meetup request
@path_2.route("/meetups/<int:meetup_id>/rsvps/<resp>/", methods=['POST'])
@token_required
def meetup_rsvp(specific_user, meetup_id, resp):
    username_len = utils.decode_token()
    username = username_len['username']
    user = UserModel.get_user_by_username(username)
    try:
        user = user[0]
    except:
        return jsonify({
            'status': 401,
            'error': "Please login first"}), 401

    if resp not in ["yes", "no", "maybe"]:
        return jsonify({
            'status':400,
            'error':'Response should be either yes, no or maybe'}), 400
    meetup = MeetupModel.get_specific_meetup(meetup_id)
    if not meetup:
        return jsonify({
            'status': 404,
            'error':'Meetup with id {} not found'.format(meetup_id)}), 404

    user_id = user['user_id']
    meetup = meetup[0]
    if resp == 'yes':
        rsvpd = utils.check_if_rsvp_already_exists(meetup_id, user_id)
        if rsvpd:
            abort(make_response(jsonify({'status': 409,
                                         'error': 'Already confirmed attendance'}), 409))

        rsvp = UserRsvp(meetup_id=meetup_id,
                    user_id=user_id,
                    meetup_topic=meetup['topic'],
                    rsvp=resp)
        rsvp.save_rsvp()

    if resp == 'no':
        rsvpd = utils.check_if_rsvp_already_exists(meetup_id, user_id)
        if rsvpd:
            UserRsvp.update_rsvp(meetup_id, user_id)
    
    # return a json formatted data
    return jsonify({'status':200, 'data':[{'meetup':meetup_id,
                                           'topic':meetup['topic'],
                                           'Attending':resp}]}), 200

# admin delete meetup
@path_2.route("/meetups/<int:meetup_id>", methods=['DELETE'])
@token_required
def admin_delete_a_meetup(specific_user, meetup_id):
    admin = utils.check_if_user_is_admin()
    if not admin:
        return jsonify({
            'status': 401,
            'error': "You are not allowed to perfom this function"}), 401

    deleted = MeetupModel.delete_specific_meetup(meetup_id)

    if deleted:
        return jsonify({'status': 200, 'data': "Meetup record deleted successfully"}), 200
    return jsonify({
        'status': 404,
        'error': "Meetup with id {} not found".format(meetup_id)}), 404