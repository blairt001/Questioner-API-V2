"""
The admin meetup model
"""
#import date
import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin import db

#assign meetups_len, questions_len, comments_len and users_len to an empty list
MEETUPS_LEN = []
QUESTIONS_LEN = []
COMMENTS_LEN = []
USERS_LEN = []

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
            '{}', '{}', '{}', '{}', '{}' , {} 
        )""".format(self.topic, self.happenningOn, self.location, self.images, self.tags, self.created_at)

        db.query_db_no_return(query)

    @staticmethod
    def get_specific_meetup(meeting_id):
        """
        get a specific meetup record using its meetup id
        """
        return [MeetupModel.to_json(meetup) for meetup in MEETUPS_LEN if meetup.id == meeting_id]

    @staticmethod
    def get_all_upcoming_meetups():
        """
        gets all meetups
        """
        return [MeetupModel.to_json(meetup) for meetup in MEETUPS_LEN]

    #delete a specific meetup
    @staticmethod
    def delete_specific_meetup(meet_id):
        found = None
        for meetup in MEETUPS_LEN:
            if meetup.id == meet_id:
                MEETUPS_LEN.remove(meetup)
                found = True
            elif meetup.id != meet_id:
                found = False
        return found

    #staticmethod decorator
    #convert the meetup record to JSON format
    #let the dict be readable
    #Ignore images and created_at
    @staticmethod
    def to_json(meetup):
        return {
            "id": meetup.id,
            "topic": meetup.topic,
            "happenningOn": meetup.happenningOn,
            "location": meetup.location,
            "tags": meetup.tags,
        }

class QuestionModel:
    def __init__(self, title, body, meetup_id):
        """
        The initialization of the Question class that defines its variables
        """
        #self.question_id = len(QUESTIONS_LEN)+1
        self.meetup_id = meetup_id
        self.title = title
        self.votes = 0
        self.body = body
        self.comments = COMMENTS_LEN
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the question store
        """
        QUESTIONS_LEN.append(self)

    @staticmethod
    def to_json(question):
        """
        format question object to a readable dictionary
        """
        return {
            "question_id": question.question_id,
            "title": question.title,
            "meetup_id": question.meetup_id,
            "votes": question.votes,
            "body": question.body,
            "comments": question.comments
        }
    @staticmethod
    def get_question(quiz_id):
        """
        fetch a specific question using its id
        """
        return [QuestionModel.to_json(question) for question in QUESTIONS_LEN if question.question_id == quiz_id]

    @staticmethod
    def get_all_questions(meeting_id):
        """
        user get all questions asked for the meetup
        """
        return [QuestionModel.to_json(question) for question in QUESTIONS_LEN if question.meetup_id == meeting_id]
#Comment model class
class CommentModel:
    """
    This is the model class for holding comment fields
    """

    def __init__(self, comment, question_id):
        self.comment = comment
        self.comment_id = len(COMMENTS)+1
        self.question_id = question_id

    def save_comment(self):
        """
        Save the comment to the comments structure
        """
        COMMENTS_LEN.append(self)

    
    @staticmethod    #module level function
    def to_json(comment):
        """
        Convert the comment object to json, a readable dict
        """
        return {"comment":comment.comment,
                "comment_id":comment.comment_id,
                "question_id":comment.question}

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
    