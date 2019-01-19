"""
The admin meetup model
"""
#import date
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin import db

#assign meetups_len, questions_len, comments_len and users_len to an empty list
"""
MEETUPS_LEN = []
QUESTIONS_LEN = []
COMMENTS_LEN = []
USERS_LEN = []
"""

#create the meetup model class
class MeetupModel:
    def __init__(self, topic, happenningOn, location, images, tags):
        """
       Initialize the meetup class, with your variables at hand
        """
       # self.id = len(MEETUPS_LEN)+1
        self.topic = topic
        self.happenningOn = happenningOn
        self.location = location
        self.images = images
        self.tags = tags
        self.created_at = datetime.now()


    def save_meetup_record(self):
        """
        save a new meetup record to the postgres database
        """
        #MEETUPS_LEN.append(self)
        query = """
        INSERT INTO meetups(topic, happenningOn, meetup_location, meetup_images, meetup_tags, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}' , '{}'
        )""".format(self.topic, self.happenningOn, self.location, self.images, self.tags, self.created_at)

        db.query_db_no_return(query)

    @staticmethod
    def get_specific_meetup(meeting_id):
        """
        get a specific meetup record using its meeting id
        """
        #return [MeetupModel.to_json(meetup) for meetup in MEETUPS_LEN if meetup.id == meeting_id]
        query = """
        SELECT meetup_id, topic, happenningOn, meetup_location FROM meetups
        WHERE meetups.meetup_id = '{}'""".format(meeting_id)

        meetup = database.select_from_db(query)
        return meetup

    @staticmethod
    def get_all_upcoming_meetups():
        """
        gets all meetups
        """
        #return [MeetupModel.to_json(meetup) for meetup in MEETUPS_LEN]

        query = """
        SELECT meetup_id, topic, meetup_date, meetup_location,
        meetup_tags, created_at FROM meetups
        """

        meetups = database.select_from_db(query)
        data = []
        for meetup in meetups:
            meetup = {'meetupId' : meetup["meetup_id"],
                      'topic' : meetup["topic"],
                      'HappenningOn' : meetup["happenningOn"],
                      'meetupLocation' : meetup["meetup_location"],
                      'meetupTags' : meetup["meetup_tags"],
                      'createdAt' : meetup["created_at"]}
            data.append(meetup)

        return data

    #delete a specific meetup
    @staticmethod
    def delete_specific_meetup(meet_id):
        """
        found = None
        for meetup in MEETUPS_LEN:
            if meetup.id == meet_id:
                MEETUPS_LEN.remove(meetup)
                found = True
            elif meetup.id != meet_id:
                found = False
        return found
        """

        meetup = MeetupModel.get_meetup(meet_id)

        if meetup:
            query = """
            DELETE FROM meetups
            WHERE meetups.meetup_id = '{}'""".format(meet_id)

            database.query_db_no_return(query)
            return True
        return False

    #check if a meetup already exists
    @staticmethod
    def check_if_meetup_already_posted(meetup_location, date):
        query = """
        SELECT meetup_id FROM meetups
        WHERE meetups.meetup_location = '{}' AND meetups.meetup_date = '{}'
        """.format(meetup_location, date)

        posted = database.select_from_db(query)
        return posted


    #staticmethod decorator
    #convert the meetup record to JSON format
    #let the dict be readable
    #Ignore images and created_at
    """
    @staticmethod
    def to_json(meetup):
        return {
            "id": meetup.id,
            "topic": meetup.topic,
            "happenningOn": meetup.happenningOn,
            "location": meetup.location,
            "tags": meetup.tags,
        }
    """

class QuestionModel:
    def __init__(self ,user_id, title, body, meetup_id, votes = 0):
        """
        The initialization of the Question class that defines its variables
        """
        #self.question_id = len(QUESTIONS_LEN)+1
        self.user_id = user_id
        self.meetup_id = meetup_id
        self.title = title
        self.votes = 0
        self.body = body
        #self.comments = COMMENTS_LEN
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the question store
        """
        #QUESTIONS_LEN.append(self)
        query = """
        INSERT INTO questions(user_id, meetup_id, title,
                              body, votes, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.user_id, self.meetup_id, self.title,
                    self.body, self.votes, self.created_at)

        database.query_db_no_return(query)
    """
    @staticmethod
    def to_json(question):
        return {
            "question_id": question.question_id,
            "title": question.title,
            "meetup_id": question.meetup_id,
            "votes": question.votes,
            "body": question.body,
            "comments": question.comments
        }
    """

    @staticmethod
    def get_question(quiz_id):
        """
        fetch a specific question using its id
        """
        #return [QuestionModel.to_json(question) for question in QUESTIONS_LEN if question.question_id == quiz_id]
        query = """
        SELECT question_id, title, body, comment, votes FROM questions
        WHERE questions.question_id = '{}'""".format(quiz_id)

        question = database.select_from_db(query)
        return question


    @staticmethod
    def get_all_questions(meeting_id):
        """
        user get all questions asked for the meetup
        """
        #return [QuestionModel.to_json(question) for question in QUESTIONS_LEN if question.meetup_id == meeting_id]
        query = """
        SELECT question_id, user_id, meetup_id, title,
        body, votes, created_at FROM questions
        WHERE questions.meetup_id = '{}'
        """.format(meeting_id)

        questions = database.select_from_db(query)
        data = []
        for question in questions:
            question = {'questionId' : question["question_id"],
                        'userId' : question["user_id"],
                        'meetupId' : question["meetup_id"],
                        'title' : question["title"],
                        'body' : question["body"],
                        'votes' : question["votes"],
                        'createdAt' : question["created_at"]
                       }
            data.append(question)

        return data

#Comment model class
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
        Save the comment to postgres database
        """
        #COMMENTS_LEN.append(self)
        query = """
        INSERT INTO comments(user_id, question_id, title, body, comment) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )""".format(self.user_id, self.question_id, self.title,
                    self.body, self.comment)

        database.query_db_no_return(query)

    @staticmethod
    def get_all_comments(quiz_id):
        """
        get all the comments for a given question
        """
        query = """
        SELECT user_id, question_id, title, body, comment FROM comments
        WHERE comments.question_id = '{}'
        """.format(quiz_id)

        comments = database.select_from_db(query)
        data = []
        for comment in comments:
            comment = {'userId' : comment["user_id"],
                       'questionId' : comment["question_id"],
                       'title' : comment["title"],
                       'body' : comment["body"],
                       'comment' : comment["comment"],
                      }
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
        #self.user_id = len(USERS_LEN)+1
        #self.firstname = firstname
        #self.lastname = lastname
        #self.username = username
        #self.email = email
        #self.registered_on = datetime.now()
        #self.password = password
        #self.is_admin = False

        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone = phone
        self.password = self.encrypt_password_on_signup(password)
    #after sign-up save the user to the created dict , USERS_LEN
    def save_user(self):
        """
        Add a new user to the users store
        """
        #USERS_LEN.append(self)
        query = """
        INSERT INTO users(username, firstname, lastname, phone, email, password) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname, self.phone, self.email, self.password)

        db.query_db_no_return(query)

    #lets check the data store for any user
    @staticmethod
    def query_users(username, password):
        #return [UserModel.to_json(user) for user in USERS_LEN if user.username == username and user.password == password]
        query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.username = '{}'""".format(username)

        return db.select_from_db(query)

    #get the user using his / her username
    @staticmethod
    def get_user_by_username(username):
        query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.username = '{}'""".format(username)

        return db.select_from_db(query)

    #Ensure password is hashed password on the sign-in
    def encrypt_password_on_signup(self, password):
        hashed_password = generate_password_hash(str(password))
        return hashed_password
    
    #check if password exists in the database, if they match
    @staticmethod
    def check_if_password_in_db(password_hash, password):
        return check_password_hash(password_hash, str(password))

    @staticmethod
    def get_user_questions(user_id):
        query = """
        SELECT question_id FROM questions
        WHERE questions.user_id = '{}'""".format(user_id)

        questions_list = database.select_from_db(query)
        questions = len(questions_list)
        return questions

    @staticmethod
    def get_user_meetups(user_id):
        query = """
        SELECT meetup_id, meetup_topic FROM rsvps
        WHERE rsvps.user_id = '{}' AND rsvps.rsvp = '{}'
        """.format(user_id, 'yes')

        meetups = database.select_from_db(query)
        return meetups

    @staticmethod
    def to_json(user):
        """
        format user object to a readable dictionary
        """
        return {"username": user.username,
                "email": user.email,
                "password": user.password,}
    #return a json data , a readable dictionary object, including the date user was registered
   
    #older return
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
        query = """
        INSERT INTO rsvps(meetup_id, user_id, meetup_topic, rsvp) VALUES(
            '{}', '{}', '{}', '{}'
        )""".format(self.meetup_id, self.user_id, self.meetup_topic, self.rsvp)

        database.query_db_no_return(query)


    @staticmethod
    def update_rsvp(meetup_id, user_id):
        """
        remove a yes response when the same user cancels attendance
        """
        query = """
        UPDATE rsvps SET rsvp = '{}' WHERE rsvps.meetup_id = '{}'
        AND rsvps.user_id = '{}'
        """.format('no', meetup_id, user_id)

        database.query_db_no_return(query)


    @staticmethod
    def get_attendees(meetup_id):
        """
        Get the number of people who have confirmed to attend a meetup
        """
        query = """
        SELECT rsvp_id FROM rsvps
        WHERE rsvps.meetup_id = '{}' AND rsvps.rsvp = '{}'
        """.format(meetup_id, 'yes')

        attendees_list = database.select_from_db(query)
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
        Save the votes to database
        """
        query = """
        INSERT INTO votes(user_id, question_id) VALUES(
            '{}', '{}'
        )""".format(self.user_id, self.question_id)

        database.query_db_no_return(query)

     #check if a user already voted
    @staticmethod
    def check_if_already_voted(user_id, question_id):
        query = """
        SELECT user_id, question_id FROM votes
        WHERE votes.user_id = '{}' AND votes.question_id = '{}'
        """.format(user_id, question_id)

        voted = database.select_from_db(query)
        return voted

class AuthToken:
    """
    The authorization token class
    """
    def __init__(self, token):
        self.token = token

    def blacklist_token(self):
        query = """
        INSERT INTO blacklist_tokens(token) VALUES(
            '{}'
        )""".format(self.token)

        database.query_db_no_return(query)

    @staticmethod
    def check_if_token_blacklisted(token):
        query = """
        SELECT token FROM blacklist_tokens
        WHERE blacklist_tokens.token = '{}'
        """.format(token)

        token = database.select_from_db(query)
        return token  