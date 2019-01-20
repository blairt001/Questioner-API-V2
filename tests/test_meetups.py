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
                             "lastname": "Blair",
                             "phoneNumber":"0715096908",
                             "username":"admin",
                             "email":"admin@gmail.com",
                             "password": "andela2019",
                             "confirmpassword":"andela2019"}

        self.signup_user1 = {"firstname":"Tony",
                             "lastname": "Andela",
                             "phoneNumber":"0713403687",
                             "username":"fakeadmin",
                             "email":"blairtdev@gmail.com",
                             "password": "Blairman1234",
                             "confirmpassword":"Blairman1234"}

        self.login_admin1 = {"username":"admin",
                           "password":"andela2019"}

        self.login_user1 = {"username":"fakeadmin",
                           "password":"Blairman1234"}



        self.post_meetup1 = {"topic":"Scrum",
                            "happenningon":"14/02/2019",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"
                           }
        self.post_meetup2 = {"topic":"Fullstack",
                             "happenningon":"15/02/2019",
                             "location":"Nairobi",
                             "images": "tony.png",
                             "tags":"Health"
                            }
        self.post_meetup3 = {"topic":"Miguel Miguel",
                             "happenningon":"16/02/2019",
                             "location":"Nairobi",
                             "images":"Miguel.png",
                             "tags":"Tech"
                            }

        self.rsvp_response1 = [{"Attending": "yes",
                                "meetup": 1,
                                "topic": "Scrum"}]

        self.meetup_topic_record = {"topic":"",
                            "happenningon":"14/02/2019",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"}

        self.meetup_location_record = {"topic":"Scrum",
                            "happenningon":"14/02/2019",
                            "location":"",
                            "images":"blair.png",
                            "tags":"Tech"}

        self.meetup_date_record = {"topic":"Scrum",
                            "happenningon":"",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":"Tech"}

        self.meetup_tag_record = {"topic":"Scrum",
                            "happenningon":"14/02/2019",
                            "location":"Thika",
                            "images":"blair.png",
                            "tags":""}

        self.check_whitespace = {"topic":"Scrum",
                                 "happenningon":"14/02/2019",
                                 "location":"              ",
                                 "images":"blair.png",
                                 "tags": "Tech"}



        self.meetups = [{"created_at": "Wed, 09 Jan 2019 02:30:10 GMT",
                         "id": 1,
                         "images": ["blair.png",
                                    "tony.png"],
                         "location": "Thika",
                         "happenningon": "2019-02-14",
                         "tags": "Tech",
                         "topic": "Scrum"},
                        {"created_at": "Wed, 09 Jan 2019 02:30:54 GMT",
                         "id": 2,
                         "images": "tony.png",
                         "location": "Nairobi",
                         "happenningon": "2019-02-15",
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
    def user_login(self):
        #since we had already registered the admin user
        login = self.client.post('api/v2/auth/login',
                                 data=json.dumps(self.login_admin1),
                                 content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token

    #tests admin create meetup
    def test_admin_can_create_a_meetup(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.post_meetup1),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{
            "location": "Thika",
            "happenningon": "14 Feb 2019",
            "tags": "Tech",
            "topic": "Scrum"
        }])

    #tests for meetup not set
    def test_no_meetup_topic_provided(self):
        self.token = self.user_login()
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
        self.token = self.user_login()
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
        self.token = self.user_login()
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
        self.token = self.user_login()
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
        token =resp['token']
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.post_meetup1),
                                    headers={'x-access-token': token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["status"], 401)
        self.assertEqual(result["error"], "You are not allowed to perfom this function")

    #tests for any available whitespaces
    def test_if_a_user_inputs_a_whitespace(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.check_whitespace),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'location field cannot be left blank')

     #tests that user can get a single meetup record
    def test_user_can_get_a_single_meetup_record(self):
         
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.get("api/v2/meetups/1",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['data'], {'meetupId': 1,
                                          'topic':"Scrum",
                                          'happenningon': "Thu, 14 Feb 2019 00:00:00 GMT",
                                          'location':"Thika"})

    #tests if a user can be able to get all meetup records
    def test_a_user_can_be_able_to_get_all_meetup_records(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")

        response = self.client.get("api/v2/meetups/upcoming",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["status"], 200)
        self.assertTrue(result["data"])

    #tests admin can delete a meetup record
    def test_admin_can_delete_a_meetup_record(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.delete("api/v2/meetups/1",
                                      headers={'x-access-token': self.token},
                                      content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["data"], "Meetup record deleted successfully")

