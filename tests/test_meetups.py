"""Tests for meetups records"""
#imports
import os
import unittest
import json
 
from app import create_app
from config import app_config
from app.admin.db import init_db
class MeetupsBaseTest(unittest.TestCase):

    def setUp(self):

        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL'] #getting database config from the env file
        init_db(self.DB_URL) #getting our database url from the env file

        self.signup_admin1 = {"firstname":"Tony",
                             "lastname": "Andela",
                             "phoneNumber":"0715096908",
                             "username":"blairtheadmin",
                             "email":"blair1234@gmail.com",
                             "password": "Blairman1234",
                             "confirmpassword":"Blairman1234"}

        self.signup_user1 = {"firstname":"Tony",
                             "lastname": "Andela",
                             "phoneNumber":"0713403687",
                             "username":"fakeadmin",
                             "email":"blair1234.dev@gmail.com",
                             "password": "Blairman1234",
                             "confirmpassword":"Blairman1234"}

        self.login_admin1 = {"username":"blairtheadmin",
                           "password":"Blairman1234"}

        self.login_user1 = {"username":"fakeadmin",
                           "password":"Blairman1234"}



        self.post_meetup1 = {"topic":"Scrum",
                            "happenningOn":"2019-02-14",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"
                           }
        self.post_meetup2 = {"topic":"Fullstack",
                             "happenningOn":"2019-02-15",
                             "location":"Nairobi",
                             "images": "tony.png",
                             "tags":"Health"
                            }
        self.post_meetup3 = {"topic":"Miguel Miguel",
                             "happenningOn":"2019-02-16",
                             "location":"Nairobi",
                             "images":"Miguel.png",
                             "tags":"Tech"
                            }

        self.rsvp_response1 = [{"Attending": "yes",
                                "meetup": 1,
                                "topic": "Scrum"}]

        self.meetup_topic_record = {"topic":"",
                            "happenningOn":"14/02/2019",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"}

        self.meetup_location_record = {"topic":"Scrum",
                            "happenningOn":"14/02/2019",
                            "location":"",
                            "images":"blair.png",
                            "tags":"Tech"}

        self.meetup_date_record = {"topic":"Scrum",
                            "happenningOn":"",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"}

        self.meetup_tag_record = {"topic":"Scrum",
                            "happenningOn":"14/02/2019",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":""}


        self.meetups = [{"created_at": "Wed, 09 Jan 2019 02:30:10 GMT",
                         "id": 1,
                         "images": ["blair.png",
                                    "tony.png"],
                         "location": "Thika",
                         "happenningOn": "2019-02-14",
                         "tags": "Tech",
                         "topic": "Scrum"},
                        {"created_at": "Wed, 09 Jan 2019 02:30:54 GMT",
                         "id": 2,
                         "images": "tony.png",
                         "location": "Nairobi",
                         "happenningOn": "2019-02-15",
                         "tags": "Health",
                         "topic": "Fullstack"
                        }]
        #use an empty token for performing the tests
        self.token = ''

    #tear down tests                                 
    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False  
        init_db(self.DB_URL)  

class TestMeetupsRecords(MeetupsBaseTest):
    """
    We test for all the meetup endpoints
    """
    def login(self):
        """
       login to perform the operations
        """
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(self.signup_admin1),
                         content_type="application/json")
        login = self.client.post('api/v2/auth/login',
                                 data=json.dumps(self.login_admin1),
                                 content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token
    """
    #tests admin create meetup
    def test_admin_can_create_a_meetup(self):
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.post_meetup1),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{"topic":"Scrum",
                            "happenningOn":"2019-02-14",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"
                           }])
    """
    #tests for meetup not set
    def test_no_meetup_topic_provided(self):
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
        data = json.dumps(self.meetup_topic_record),
        headers={'x-access-token': self.token},
        content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'Provide the topic field')
    
    #tests for meetup location missing
    def test_no_meetup_location_provided(self):
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetup_location_record),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'provide the location')
    #tests for meetup date missing
    def test_no_meetup_date_provided(self):
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetup_date_record),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'provide the meetup date')

    #tests for meetup tags missing
    def test_no_meetup_tags_provided(self):
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetup_tag_record),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'provide the tags')

    #lets test user can not create a meetup
    def test_user_cannot_reate_a_meetup(self):
        self.client.post("api/v2/auth/signup",
                         data = json.dumps(self.signup_user1),
                         content_type = "application/json")
        login = self.client.post("api/v2/auth/login",
                                 data = json.dumps(self.login_user1),
                                 content_type = "application/json")
        resp = json.loads(login.data.decode('utf-8'))
        user_token =resp['token']
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.post_meetup1),
                                    headers={'x-access-token': user_token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["status"], 401)
        self.assertEqual(result["error"], "You are not allowed to perfom this function")