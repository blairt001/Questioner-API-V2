"""Tests for questions records"""
import json
import unittest

from app import create_app
from config import app_config
from app.admin.db import init_db
class QuestionBaseTest(unittest.TestCase):
    """
    Setting up tests
    """

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL'] 
        init_db(self.DB_URL)

        self.signup_user1 = {"firstname": "Tony",
                             "lastname": "Blair",
                             "phoneNumber": "0715096908",
                             "username": "admin",
                             "email": "admin@gmail.com",
                             "password": "Andela2019",
                             "confirmpassword": "Andela2019"}

        self.signup_user2 = {"firstname": "Tony",
                             "lastname": "Andela",
                             "phoneNumber": "0715096908",
                             "username": "fakeadmin",
                             "email": "blaidev@gmail.com",
                             "password": "Blairman1234",
                             "confirmpassword": "Blairman1234"}

        self.login_user_1 = {"username": "admin",
                             "password": "Andela2019"}

        self.login_user_2 = {"username": "fakeadmin",
                             "password": "Blairman1234"}

        self.post_meetup1 = {"topic": "Scrum",
                             "happenningon": "14/02/2019",
                             "location": "Thika",
                             "images": "blair.png",
                             "tags": "Tech"}

        self.post_question1 = {"title": "What is Dev?",
                               "body": "I really like how people talk about Tonys Dev"}

        self.post_question2 = {"title": "What is JWT?",
                               "body": "I learnt more about JWT at Bootcamp"}

        self.post_question3 = {"title": "Hey Mehn?",
                               "body": "It is just OK"}

        self.upvoted_question = {"body": "I really like how people talk about Tonys Dev",
                                 "comment": "",
                                 "questionid": 1,
                                 "title": "What is Dev?",
                                 "votes": 1}
        self.downvoted_question = {"body": "I really like how people talk about Tonys Dev",
                                   "comment": "",
                                   "questionid": 1,
                                   "title": "What is Dev?",
                                   "votes": -1}
        self.downvoted_question2 = {"body": "I learnt more about JWT at Bootcamp",
                                   "comment": "",
                                   "questionid": 1,
                                   "title": "What is JWT?",
                                   "votes": -1}
                                   
        # prepare comments setup to accelerate our tests
        self.post_comment1 = {"comment": "Wow, I love every topic on Dev"}

        self.question1_and_comment1 = {"body": "I really like how people talk about Tonys Dev",
                                       "comment": "Wow, I love every topic on Dev",
                                       "question_id": 1,
                                       "title": "What is Dev?",
                                       "userId": 1}

        self.token = ''
    # tear down tests  
                                   
    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False
        init_db(self.DB_URL) 


class TestQuestionApiEndpoint(QuestionBaseTest):
    # create an empty token on admin login
    def user_login(self):
        login = self.client.post('api/v2/auth/login',
                                 data=json.dumps(self.login_user_1),
                                 content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token

    # tests user can post a question to a specific meetup
    def test_user_can_post_a_question_to_meetup_record(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['data'],
                         [{"body": "I really like how people talk about Tonys Dev",
                           "meetup": 1,
                           "title": "What is Dev?",
                           "user_id": 1}])
   
    # test user get all question records
    def test_user_get_all_questions_records(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.get("api/v2/meetups/1/questions",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    # test user comment on a given question
    def test_user_comment_on_a_given_question(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/questions/1/comment",
                                    data=json.dumps(self.post_comment1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf'8"))
        self.assertEqual(result['data'], self.question1_and_comment1)

    # tests user can get all comments
    def test_user_can_get_all_comments_on_question_record(self):
        self.token = self.user_login()
        first = self.client.post("api/v2/meetups",
                                 data=json.dumps(self.post_meetup1),
                                 headers={'x-access-token': self.token},
                                 content_type="application/json")
        self.assertEqual(first.status_code, 201)
        second = self.client.post("api/v2/meetups/1/questions",
                                  data=json.dumps(self.post_question1),
                                  headers={'x-access-token': self.token},
                                  content_type="application/json")
        self.assertEqual(second.status_code, 201)
        third = self.client.post("api/v2/questions/1/comment",
                                 headers={'x-access-token': self.token},
                                 data=json.dumps(self.post_comment1),
                                 content_type="application/json")
        self.assertEqual(third.status_code, 201)
        response = self.client.get("api/v2/questions/1/comments",
                                   headers={'x-access-token': self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    # tests user can upvote a question
    def test_user_can_upvote_question(self):
        self.token = self.user_login()
        first = self.client.post("api/v2/meetups",
                                 data=json.dumps(self.post_meetup1),
                                 headers={'x-access-token': self.token},
                                 content_type="application/json")
        self.assertEqual(first.status_code, 201)
        second = self.client.post("api/v2/meetups/1/questions",
                                  data=json.dumps(self.post_question1),
                                  headers={'x-access-token': self.token},
                                  content_type="application/json")
        self.assertEqual(second.status_code, 201)
        response = self.client.patch("api/v2/questions/1/upvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.upvoted_question)

    # tests user can downvote a question
    def test_user_can_downvote_a_question_record(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.patch("api/v2/questions/1/downvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.downvoted_question)
  
    # prevent a user from voting a question more than once
    def test_user_upvote_question_more_than_once(self):
        self.token = self.user_login()
        first = self.client.post("api/v2/meetups",
                                 data=json.dumps(self.post_meetup1),
                                 headers={'x-access-token': self.token},
                                 content_type="application/json")
        self.assertEqual(first.status_code, 201)
        second = self.client.post("api/v2/meetups/1/questions",
                                  data=json.dumps(self.post_question1),
                                  headers={'x-access-token': self.token},
                                  content_type="application/json")
        self.assertEqual(second.status_code, 201)
        self.client.patch("api/v2/questions/1/upvote",
                          headers={'x-access-token': self.token},
                          content_type="application/json")
        response = self.client.patch("api/v2/questions/1/upvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 409)

        # tests for unavailable meetup
    def test_no_meetup_found(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups/20/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 404)
        self.assertEqual(result['error'], 'No meetup with id 20 found')
