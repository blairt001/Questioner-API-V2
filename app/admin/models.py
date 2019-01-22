"""
The admin meetup model
"""

# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.admin import db


# create the meetup model class
class MeetupModel:
    def __init__(self, topic, happenningon, location, images, tags):
        """
       Initialize the meetup class, with your variables at hand
        """
        # self.id = len(MEETUPS_LEN)+1
        self.topic = topic
        self.happenningon = happenningon
        self.location = location
        self.images = images
        self.tags = tags
        self.created_at = datetime.now()

    def save_meetup_record(self):
        """
        save a new meetup record to the postgres db
        """
        # MEETUPS_LEN.append(self)
        insert_query = """
        INSERT INTO meetups(topic, happenningon, meetup_location, meetup_images, meetup_tags, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}' , '{}'
        )""".format(self.topic, self.happenningon, self.location, self.images, self.tags, self.created_at)

        db.query_data_from_db(insert_query)

    @staticmethod
    def get_specific_meetup(meeting_id):
        """
        get a specific meetup record using its meeting id
        """
        # return [MeetupModel.to_json(meetup) for meetup in MEETUPS_LEN if meetup.id == meeting_id]
        select_specific_query = """
        SELECT meetup_id, topic, happenningon, meetup_location FROM meetups
        WHERE meetups.meetup_id = '{}'""".format(meeting_id)

        meetup = db.select_data_from_db(select_specific_query)
        return meetup

    @staticmethod
    def get_all_upcoming_meetups():
        """
        gets all meetups
        """
        # return [MeetupModel.to_json(meetup) for meetup in MEETUPS_LEN]

        select_all_meetup_query = """
        SELECT meetup_id, topic, happenningon, meetup_location,
        meetup_tags, created_at FROM meetups
        """

        meetups = db.select_data_from_db(select_all_meetup_query)
        data = []
        for meetup in meetups:
            meetup = {'meetupId': meetup["meetup_id"],
                      'topic': meetup["topic"],
                      'happenningon': meetup["happenningon"],
                      'meetupLocation': meetup["meetup_location"],
                      'meetupTags': meetup["meetup_tags"],
                      'createdAt': meetup["created_at"]}
            data.append(meetup)

        return data

    # delete a specific meetup
    @staticmethod
    def delete_specific_meetup(meeting_id):
        """
        found = None
        for meetup in MEETUPS_LEN:
            if meetup.id == meeting_id:
                MEETUPS_LEN.remove(meetup)
                found = True
            elif meetup.id != meeting_id:
                found = False
        return found
        """
        # get specific meetup
        meetup = MeetupModel.get_specific_meetup(meeting_id)

        if meetup:
            delete_query = """
            DELETE FROM meetups
            WHERE meetups.meetup_id = '{}'""".format(meeting_id)

            db.query_data_from_db(delete_query)
            return True
        return False

    # check if a meetup already exists
    @staticmethod
    def check_if_meetup_already_posted(meetup_location, date):
        query = """
        SELECT meetup_id FROM meetups
        WHERE meetups.meetup_location = '{}' AND meetups.happenningon = '{}'
        """.format(meetup_location, date)

        posted = db.select_data_from_db(query)
        return posted

    # staticmethod decorator
    # convert the meetup record to JSON format
    # let the dict be readable
    # Ignore images and created_at
    """
    @staticmethod
    def to_json(meetup):
        return {
            "id": meetup.id,
            "topic": meetup.topic,
            "happenningon": meetup.happenningon,
            "location": meetup.location,
            "tags": meetup.tags,
        }
    """


class QuestionModel:
    def __init__(self, user_id, title, body, meetup_id, votes=0):
        """
        The initialization of the Question class that defines its variables
        """
        # self.question_id = len(QUESTIONS_LEN)+1
        self.user_id = user_id
        self.meetup_id = meetup_id
        self.title = title
        self.votes = 0
        self.body = body
        self.comment = ""
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the database
        """
        insert_question_query = """
        INSERT INTO questions(user_id, meetup_id, title, body, votes, comment, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.user_id, self.meetup_id, self.title, self.body, self.votes, self.comment, self.created_at)

        db.query_data_from_db(insert_question_query)

    @staticmethod
    def get_question(quiz_id):
        """
        fetch a specific question using its id
        """
        # return [QuestionModel.to_json(question) for question in QUESTIONS_LEN if question.question_id == quiz_id]
        get_question_query = """
        SELECT question_id, title, body, comment, votes FROM questions
        WHERE questions.question_id = '{}'""".format(quiz_id)

        question = db.select_data_from_db(get_question_query)
        return question

    @staticmethod
    def get_all_questions(meet_id):
        """
        user get all questions asked for the meetup
        """
        # return [QuestionModel.to_json(question) for question in QUESTIONS_LEN if question.meetup_id == meeting_id]
        get_all_questions_query = """
        SELECT question_id, user_id, meetup_id, title,
        body, votes, created_at FROM questions
        WHERE questions.meetup_id = '{}'
        """.format(meet_id)

        questions = db.select_data_from_db(get_all_questions_query)
        data = []
        for question in questions:
            question = {'questionId': question["question_id"],
                        'userId': question["user_id"],
                        'meetupId': question["meetup_id"],
                        'title': question["title"],
                        'body': question["body"],
                        'votes': question["votes"],
                        'createdAt': question["created_at"]}
            data.append(question)

        return data


# Comment model class
class CommentModel:
    """
    This is the model class for holding comment fields
    """

    def __init__(self, title, body, comment, user_id, question_id):
        self.title = title
        self.body = body
        self.comment = comment
        self.user_id = user_id
        self.question_id = question_id

    def save_comment(self):
        """
        Save the comment to postgres db
        """
        # COMMENTS_LEN.append(self)
        save_comment_query = """
        INSERT INTO comments(user_id, question_id, title, body, comment) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )""".format(self.user_id, self.question_id, self.title,
                    self.body, self.comment)

        db.query_data_from_db(save_comment_query)

    @staticmethod
    def get_all_comments(quiz_id):
        """
        get all the comments for a given question
        """
        get_all_comments_query = """
        SELECT user_id, question_id, title, body, comment FROM comments
        WHERE comments.question_id = '{}'
        """.format(quiz_id)

        comments = db.select_data_from_db(get_all_comments_query)
        data = []
        for comment in comments:
            comment = {'userId': comment["user_id"],
                       'questionId': comment["question_id"],
                       'title': comment["title"],
                       'body': comment["body"],
                       'comment': comment["comment"], }
            data.append(comment)

        return data

    """
    @staticmethod    #module level function
    def to_json(comment):
        return {"comment":comment.comment,
                "comment_id":comment.comment_id,
                "question_id":comment.question}
    """


class UserModel:
    """
    This is the user model class that contains our model setup
    """

    def __init__(self, username, email, password,
                 firstname, lastname, phone):
        """
        Start by defining each user attributes to use during the tests
        Keep in mind the user is not an admin
        """
        # self.user_id = len(USERS_LEN)+1
        # self.firstname = firstname
        # self.lastname = lastname
        # self.username = username
        # self.email = email
        # self.registered_on = datetime.now()
        # self.password = password
        # self.is_admin = False

        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone = phone
        self.password = self.encrypt_password_on_signup(password)
     
    # after sign-up save the user to the created dict , USERS_LEN
    def save_user(self):
        """
        Add a new user to the users store
        """
        # USERS_LEN.append(self)
        save_user_query = """
        INSERT INTO users(username, firstname, lastname, phone, email, password) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname, self.phone, self.email, self.password)

        db.query_data_from_db(save_user_query)

    # lets check the data store for any user
    @staticmethod
    def query_users(username, password):
        # return [UserModel.to_json(user) for user in USERS_LEN if user.username == username and user.password == password]
        select_user_query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.username = '{}'""".format(username)

        return db.select_data_from_db(select_user_query)

    # get the user using his / her username
    @staticmethod
    def get_user_by_username(username):
        select_user_by_username_query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.username = '{}'""".format(username)

        return db.select_data_from_db(select_user_by_username_query)

    # Ensure password is hashed password on the sign-in
    def encrypt_password_on_signup(self, password):
        hashed_password = generate_password_hash(str(password))
        return hashed_password
    
    # check if password exists in the db, if they match
    @staticmethod
    def check_if_password_in_db(password_hash, password):
        return check_password_hash(password_hash, str(password))

    @staticmethod
    def get_user_questions(user_id):
        get_user_query = """
        SELECT question_id FROM questions
        WHERE questions.user_id = '{}'""".format(user_id)

        questions_list = db.select_data_from_db(get_user_query)
        questions = len(questions_list)
        return questions

    @staticmethod
    def get_user_meetups(user_id):
        get_user_meetups_query = """
        SELECT meetup_id, meetup_topic FROM rsvps
        WHERE rsvps.user_id = '{}' AND rsvps.rsvp = '{}'
        """.format(user_id, 'yes')

        meetups = db.select_data_from_db(get_user_meetups_query)
        return meetups

    @staticmethod
    def to_json(user):
        """
        format user object to a readable dictionary
        """
        return {"username": user.username,
                "email": user.email,
                "password": user.password, }
    # return a json data , a readable dictionary object, including the date user was registered
   
    # older return
    """
    @staticmethod
    def to_json(user):
        return {"firstname": user.firstname,
                "lastname": user.lastname,
                "username": user.username,
                "email": user.email,
                "password": user.password,
       
             "registered_on": user.registered_on,}
    """


class UserRsvp:
    """
    The rsvp models
    """

    def __init__(self, meetup_id, user_id, meetup_topic, rsvp):
        """
        The initializer function that sets the rsvp variables
        """
        self.meetup_id = meetup_id
        self.user_id = user_id
        self.meetup_topic = meetup_topic
        self.rsvp = rsvp

    def save_rsvp(self):
        """
        Save the rsvp to the rsvps store
        """
        save_rsvp_query = """
        INSERT INTO rsvps(meetup_id, user_id, meetup_topic, rsvp) VALUES(
            '{}', '{}', '{}', '{}'
        )""".format(self.meetup_id, self.user_id, self.meetup_topic, self.rsvp)

        db.query_data_from_db(save_rsvp_query)

    @staticmethod
    def update_rsvp(meetup_id, user_id):
        """
        remove a yes response when the same user cancels attendance
        """
        update_rsvp_query = """
        UPDATE rsvps SET rsvp = '{}' WHERE rsvps.meetup_id = '{}'
        AND rsvps.user_id = '{}'
        """.format('no', meetup_id, user_id)

        db.query_data_from_db(update_rsvp_query)

    @staticmethod
    def get_attendees(meetup_id):
        """
        Get the number of people who have confirmed to attend a meetup
        """
        get_attendees_query = """
        SELECT rsvp_id FROM rsvps
        WHERE rsvps.meetup_id = '{}' AND rsvps.rsvp = '{}'
        """.format(meetup_id, 'yes')

        attendees_list = db.select_data_from_db(get_attendees_query)
        attendees = len(attendees_list)
        return attendees


class UserVote:
    """
    The user votes model class
    """

    def __init__(self, question_id, user_id):
        self.question_id = question_id
        self.user_id = user_id

    def save_vote(self):
        """
        Save the votes to db
        """
        save_vote_query = """
        INSERT INTO votes(user_id, question_id) VALUES(
            '{}', '{}'
        )""".format(self.user_id, self.question_id)

        db.query_data_from_db(save_vote_query)

    # check if a user already voted
    @staticmethod
    def check_if_already_voted(user_id, question_id):
        check_vote_query = """
        SELECT user_id, question_id FROM votes
        WHERE votes.user_id = '{}' AND votes.question_id = '{}'
        """.format(user_id, question_id)

        voted = db.select_data_from_db(check_vote_query)
        return voted


class AuthToken:
    """
    The authorization token class
    """
    def __init__(self, token):
        self.token = token

    def blacklist_token(self):
        insert_blacklist_query = """
        INSERT INTO blacklist_tokens(token) VALUES(
            '{}'
        )""".format(self.token)

        db.query_data_from_db(insert_blacklist_query)

    @staticmethod
    def check_if_token_blacklisted(token):
        check_blacklist_token_query = """
        SELECT token FROM blacklist_tokens
        WHERE blacklist_tokens.token = '{}'
        """.format(token)

        token = db.select_data_from_db(check_blacklist_token_query)
        return token  