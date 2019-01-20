import json
import unittest

# local imports
from app import create_app

class QuestionBaseTest(unittest.TestCase):
    """
    Setting up tests
    """

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()


        self.signup_user1 = {"firstname":"Tony",
                             "lastname": "Blair",
                             "username":"toniezah",
                             "email":"blairt134@gmail.com",
                             "password": "Manchester123",
                             "confirm_password":"Manchester123"}

        self.signup_user2 = {"firstname":"Tony",
                             "lastname": "Andela",
                             "username":"fakeadmin",
                             "email":"blair1234.dev@gmail.com",
                             "password": "Blairman1234",
                             "confirm_password":"Blairman1234"}

        self.login_user_1 = {"username":"toniezah",
                           "password":"Manchester123"}

        self.login_user_2 = {"username":"fakeadmin",
                           "password":"Blairman1234"}


        self.meetup = {"topic":"Andela Fellowship",
                       "happenningon":"16/02/2019",
                       "location":"Nairobi",
                       "images":["mig1.png", "mig2.png"],
                       "tags":["Tech", "Health"]
                      }

        self.post_question1 = {"title":"What is Dev?",
                               "body":"I really like how people talk about Tony's Dev"}

        self.post_question2 = {"title":"What is JWT?",
                               "body":"I learnt more about JWT at Tony's bootcamp"}

        self.post_question3 = {"title":"Hey Mehn?",
                               "body":"It is just OK"}

        self.upvoted_question= {"body": "I really like how people talk about Tony's Dev",
                                "meetup_id": 1,
                                "comments": [], #initialize comments to an empty list
                                "question_id": 1,
                                "title": "What is Dev?",
                                "votes": 1}
        self.downvoted_question = {"body": "I really like how people talk about Tony's Dev",
                                   "meetup_id": 1,
                                   "comments": [],  #initialize comments to an empy list
                                   "question_id": 1,
                                   "title": "What is Dev?",
                                   "votes": -1}
        #prepare comments setup
        self.post_comment1 = {"comment":"Wow, I love every topic on Dev, the answer will help me alot"}

        self.question1_and_comment1 = {"body": "I really like how people talk about Tony's Dev",
                                     "comments": ["Wow, I love every topic on Dev, the answer will help me alot", {"username" : "toniezah"}],
                                     "meetup_id": 1,
                                     "question_id": 1,
                                     "title": "What is Dev?",
                                     "votes": 0}

        self.token = ''
    #tear down tests                                 
    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False
        
"""
class TestQuestionApiEndpoint(QuestionBaseTest):
    #create an empty token on admin login
    def user_login(self):
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user1),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_1),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token

    def test_user_can_post_a_question_to_meetup(self):
        self.token = self.user_login()
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        response = self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1), headers={'x-access-token': self.token}, content_type = "application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['data'], [{"body": "I really like how people talk about Tony's Dev",
                                           "meetup": 1,
                                           "title": "What is Dev?"}])

    def test_upvote_question(self):
        self.token = self.user_login()
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1),headers={'x-access-token': self.token}, content_type = "application/json")
        response = self.client.patch("api/v1/questions/1/upvote",headers={'x-access-token': self.token}, content_type = "application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.upvoted_question)

    def test_downvote_question(self):
        self.token = self.user_login()
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1),headers={'x-access-token': self.token}, content_type = "application/json")
        response = self.client.patch("api/v1/questions/1/downvote", headers={'x-access-token': self.token}, content_type = "application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.downvoted_question)
    
    #tests if a user enters an invalid token
    def user_enter_invalid_token(self):
        token = "tonyblai63752752846728835278rtbxcavvv"
        response = self.client.post("api/v1/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "token is expired or invalid")
    #define test case for user posting comments
    def test_user_comment_on_a_question(self):
        self.token = self.user_login()
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1),headers={'x-access-token': self.token}, content_type = "application/json")
        response = self.client.post("api/v1/questions/1/comment", data = json.dumps(self.post_comment1), headers={'x-access-token': self.token}, content_type = "application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf'8"))
        self.assertEqual(result['data'], self.question1_and_comment1)

    def test_get_all_questions_records(self):
        self.token = self.user_login()
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1), headers={'x-access-token': self.token}, content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question2),headers={'x-access-token': self.token}, content_type = "application/json")
        response = self.client.get("api/v1/meetups/1/questions", content_type = "application/json")
        self.assertEqual(response.status_code, 200)

    #tests that an unregistered user can not post a question
    def test_unregistered_user_not_post_question(self):
        response = self.client.post("api/v1/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "Token is missing")
        """