"""Tests for meetups records"""
import unittest
import json

from app import create_app
from config import app_config
from app.admin.db import init_db


class MeetupsBaseTest(unittest.TestCase):

    def setUp(self):

        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL'] 
        init_db(self.DB_URL)

        self.signup_admin1 = {"firstname": "Tony",
                              "lastname": "Blair",
                              "phoneNumber": "0715096908",
                              "username": "admin",
                              "email": "admin@gmail.com",
                              "password": "Andela2019",
                              "confirm_password": "Andela2019"}

        self.signup_user1 = {"firstname": "Tony",
                             "lastname": "Andela",
                             "phoneNumber": "0713403687",
                             "username": "fakeadmin",
                             "email": "blairtdev@gmail.com",
                             "password": "Blairman1234",
                             "confirm_password": "Blairman1234"}

        self.login_admin1 = {"username": "admin",
                             "password": "Andela2019"}

        self.login_user1 = {"username": "fakeadmin",
                            "password": "Blairman1234"}

        self.post_meetup1 = {"topic": "Scrum",
                             "happenningon": "14/02/2019",
                             "location": "Thika",
                             "images": "blair.png",
                             "tags": ["Tech"]
                             }

        self.post_meetup2 = {"topic": "Fullstack",
                             "happenningon": "15/02/2019",
                             "location": "Nairobi",
                             "images": "tony.png",
                             "tags": ["Health"]
                             }

        self.post_meetup3 = {"topic": "Miguel Miguel",
                             "happenningon": "16/02/2019",
                             "location": "Nairobi",
                             "images": "Miguel.png",
                             "tags": ["Tech"]
                             }

        self.post_meetup4 = {"topica": "Miguel Miguel",
                             "happenningoon": "16/02/2019",
                             "location": "Nairobi",
                             "images": "Miguel.png",
                             "tags": ["Tech"]
                             }

        self.rsvp_response1 = [{"Attending": "yes",
                                "meetup": 1,
                                "topic": "Scrum"}]

        self.meetup_topic_record = {"topic": "",
                                    "happenningon": "14/02/2019",
                                    "location": "Thika",
                                    "images": "blair.png",
                                    "tags": ["Tech"]}

        self.meet_location_record = {"topic": "Scrum",
                                     "happenningon": "14/02/2019",
                                     "location": "",
                                     "images": "blair.png",
                                     "tags": ["Tech" , "Health"]}

        self.meetup_date_record = {"topic": "Scrum",
                                   "happenningon": "",
                                   "location": "Thika",
                                   "images": "blair.png",
                                   "tags": ["Tech"]}

        self.meetup_tag_record = {"topic": "Scrum",
                                  "happenningon": "14/02/2019",
                                  "location": "Thika",
                                  "images": "blair.png",
                                  "tags": ""}

        self.check_whitespace = {"topic": "Scrum",
                                 "happenningon": "14/02/2019",
                                 "location": "              ",
                                 "images": "blair.png",
                                 "tags": ["Tech"]}

        self.invalid_meetup_date = {"topic": "Scrum",
                                 "happenningon": "98635637",
                                 "location": "Thika",
                                 "images": "blair.png",
                                 "tags": ["Tech"]}

        self.meetups_past_date = {"topic": "Scrum",
                                  "happenningon": "12/07/1972",
                                  "location": "Thika",
                                  "images": "blair.png",
                                  "tags": ["Tech"]}



        self.meetups = [{"created_at": "Wed, 09 Jan 2019 02:30:10 GMT",
                         "id": 1,
                         "images": ["blair.png",
                                    "tony.png"],
                         "location": "Thika",
                         "happenningon": "2019-02-14",
                         "tags": ["Tech"],
                         "topic": "Scrum"},
                        {"created_at": "Wed, 09 Jan 2019 02:30:54 GMT",
                         "id": 2,
                         "images": "tony.png",
                         "location": "Nairobi",
                         "happenningon": "2019-02-15",
                         "tags": ["Health"],
                         "topic": "Fullstack"}]

        # use an empty token for performing the tests
        self.token = ''

    # tear down tests                                 
    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False  
        init_db(self.DB_URL)  


class TestMeetupsRecords(MeetupsBaseTest):
    def user_login(self):
        # since we had already registered the admin user
        login = self.client.post('api/v2/auth/login',
                                 data=json.dumps(self.login_admin1),
                                 content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token

    # tests admin create meetup
    def test_admin_can_create_a_meetup(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertTrue(result["data"])

    # tests for meetup not set
    def test_no_meetup_topic_provided(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups", 
                                    data=json.dumps(self.meetup_topic_record),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'Provide the topic field')
    
    # tests for meetup location missing
    def test_no_meetup_location_provided(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meet_location_record),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'provide the location')

    # tests for meetup date missing
    def test_no_meetup_date_provided(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetup_date_record),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'provide the meetup date')

    # tests for meetup tags missing
    def test_no_meetup_tags_provided(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetup_tag_record),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'provide the tags')

    # lets test user can not create a meetup
    def test_user_cannot_create_a_meetup(self):
        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.signup_user1),
                         content_type="application/json")
        login = self.client.post("api/v2/auth/login",
                                 data=json.dumps(self.login_user1),
                                 content_type="application/json")
        resp = json.loads(login.data.decode('utf-8'))
        token = resp['token']
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup1),
                                    headers={'x-access-token': token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["status"], 401)
        self.assertEqual(result["error"], "You are not allowed to perfom this function")

    # tests for any available whitespaces
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

    # tests that user can get a single meetup record
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
                                          'topic': "Scrum",
                                          'happenningon': "Thu, 14 Feb 2019 00:00:00 GMT",
                                          'location': "Thika"})

    # tests if a user can be able to get all meetup records
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

    # tests admin can delete a meetup record
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

    # tests for user rsvp for  a meetup
    def test_user_can_set_rsvp_response(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/rsvps/yes",
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.rsvp_response1)

    # tests if a user inputs a whitespace 
    def test_if_a_user_inputs_whitespace(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.check_whitespace),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'location field cannot be left blank')


    def test_user_inputes_an_invalid_date(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.invalid_meetup_date),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(
            result["Error"], "Invalid date format. Should be DD/MM/YYYY")


    def test_user_inputs_a_past_date(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_past_date),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["Error"], "Date should be in the future")

    def test_a_normal_users_cannot_create_a_meetup_record(self):
        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.signup_user1),
                         content_type="application/json")
        login = self.client.post("api/v2/auth/login",
                                 data=json.dumps(self.login_user1),
                                 content_type="application/json")
        resp = json.loads(login.data.decode('utf-8'))
        user_token = resp['token']
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup1),
                                    headers={'x-access-token': user_token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["status"], 401)
        self.assertEqual(
            result["error"], "You are not allowed to perfom this function")
    
    # test a user post wrong json data
    def test_a_user_post_wrong_json_keys(self):
        self.token = self.user_login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup4),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(
            result["error"], 'Check the json keys you have used very well')

    # tests for no meetips scheduled when there are no meetups
    def test_user_dont_get_meetup_if_not_posted(self):
        response = self.client.get("api/v2/meetups/upcoming",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["status"], 404)
        self.assertEqual(
            result["error"], "No upcoming meetups available.")

    # tests admin not deleting a meetup that is not there
    def test_admin_cannot_delete_not_found_meetup(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.delete("api/v2/meetups/50",
                                      headers={'x-access-token': self.token},
                                      content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["status"], 404)
        self.assertEqual(result["error"], "Meetup with id 50 not found")
 
    # test user set wrong rsvp response
    def test_user_set_wrong_rsvp_response(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/rsvps/imightcome",
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], 'Response should be either yes, no or maybe')

    # tests user cannot rsvp a wrong meetup
    def test_user_set_rsvp_response_to_wrong_or_unknown_meetup(self):
        self.token = self.user_login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/2/rsvps/maybe",
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], 'Meetup with id 2 not found')

