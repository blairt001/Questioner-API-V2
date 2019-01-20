"""The users meetup routes endpoint polished"""

from flask import jsonify, request , abort, make_response
from app.admin.models import QuestionModel, MeetupModel, CommentModel, UserModel
from app.api.v2 import path_2
from app.admin import db
from app.utils import token_required, decode_token
from app import utils;

@path_2.route("/meetups/<int:meetup_id>/questions", methods=['POST'])
@token_required
def create_question_record(current_user, meetup_id):
    username_len = utils.decode_token()
    username = username_len['username']
    user = UserModel.get_user_by_username(username)
    try:
        user = user[0]
    except:
        return jsonify({
            'status': 400,
            'error': "Please login first"}), 400

    try:
        data = request.get_json()
        title = data['title']
        body = data['body']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            ' error': "Check your json keys. Should be topic and body"}), 400))

    utils.check_for_whitespace(data)
    meetup = MeetupModel.get_specific_meetup(meetup_id)
    if not meetup:
        abort(make_response(jsonify({
            'status': 404,
            'error': 'No meetup with id {} found'.format(meetup_id)}), 404))

    user_id = user['user_id']
    question = QuestionModel(user_id=user_id,
                        title=title,
                        body=body,
                        meetup_id=meetup_id)

    question.save_question()

    return jsonify({"status": 201,
                    "data":[{"title": title,
                             "user_id": user_id,
                             "meetup": meetup_id,
                             "body": body}]}), 201


#get all questions record
@path_2.route("/meetups/<int:meet_id>/questions", methods=['GET'])
def get_user_get_all_questions_for_a_meetup(meet_id):
    """
    User to fetch all questions for a meetup record
    """
    questions = QuestionModel.get_all_questions(meet_id)
    if questions:
        return jsonify({"status": 200, "data": questions}), 200
    return jsonify({"status": 404, "data": "We cant find a question for this meetup. No question posted yet"}), 404

#upvote a question
@path_2.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
@token_required
def upvote_question(question_id):
    """
    The upvote question route endpoint
    """
    question = QuestionModel.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['votes'] = my_question['votes'] + 1
        return jsonify({"status": 200, "data": my_question}), 200
    return jsonify({"status": 404, "error": "Question not found"}), 404

#downvote a question
@path_2.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
@token_required
def downvote_question(question_id):
    """
    The downvote question route endpoint
    """
    question = QuestionModel.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['votes'] = my_question['votes'] - 1
        return jsonify({"status": 200, "data": my_question}), 200
    return jsonify({"status": 404, "error": "Question not found"}), 404

#user should be able to post comment
@path_2.route("/questions/<int:question_id>/comment", methods=['POST'])
def user_comment_on_a_question(question_id):
    """
    User post comment endpoint route
    """
    try:
        comment = request.get_json()['comment']
    except KeyError:
        abort(make_response(jsonify({'status': 400, 'error':'Check your json key. It is comment'})))
    username = decode_token()
    question = QuestionModel.get_question(question_id)
    if question:
        my_question = question[0]
        comments = my_question['comments']
        comments.append(comment)
        comments.append(username)
        return jsonify({"status": 201, "data": my_question}), 201
    return jsonify({'status': 404, 'error':'The question you are looking for is not found'}), 404