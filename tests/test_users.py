"""Tests for the user endpoints"""

import unittest
import json
from app import create_app
from config import app_config
from app.admin.db import init_db


class UserBaseTest(unittest.TestCase):
    """
    Set up the user tests
    """

    def setUp(self):
        """
        lets declare the variables to use on the tests
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL']
        init_db(self.DB_URL)

        self.signup_user1 = {"firstname": "Tony",
                             "lastname": "Blair",
                             "phoneNumber": "0715096908",
                             "username": "blairtony",
                             "email": "blairtony@gmail.com",
                             "password": "Blairman1234",
                             "confirmpassword": "Blairman1234"}

        self.signup_user2 = {"firstname": "Lionel",
                             "lastname": "Messi",
                             "phoneNumber": "0715096908",
                             "username": "limesi",
                             "email": "limesi@gmail.com",
                             "password": "Limesi1234",
                             "confirmpassword": "Limesi123"}

        self.signup_user3 = {"firstname": "Joshua",
                             "lastname": "Ariga",
                             "username": "arigajosh",
                             "email": "ariga@gmail.com",
                             "password": "Ariga123",
                             "confirmpassword": "Ariga123"}

        self.signup_user4 = {"firstname": "Codeman",
                             "lastname": "Pragmatic",
                             "phoneNumber": "0723456789",
                             "username": "codeprag",
                             "email": "codeman@gmail.com",
                             "password": "Cod1",
                             "confirmpassword": "Cod1"}

        self.signup_user5 = {"firstname": "Codeman",
                             "lastname": "Pragmatic",
                             "phoneNumber": "0723456789",
                             "username": "codeprag",
                             "email": "codeman@gmail.com",
                             "password": "Codedsdscfsdfsfsfhchdfgvdyvhgsdvghsd",
                             "confirmpassword": "Codedsdscfsdfsfsfhchdfgvdyvhgsdvghsd"}

        self.signup_user6 = {"firstname": "Kenyan",
                             "lastname":  "Man",
                             "phoneNumber": "0715096908",
                             "username": "kenyaa",
                             "email": "kenyan@gmail",
                             "password": "@Mitcoder1",
                             "confirmpassword": "@Mitcoder1"}

        self.login_user1 = {"username": "blairtony",
                            "password": "Blairman1234"}

        self.login_user2 = {"username": "limesi",
                            "password": "Limesi1234"}

        self.login_user3 = {"username": "kenyaa",
                            "password": "@Mitcoder1"}

    # clean up the tests
    def tearDown(self):
        self.app.testing = False
        init_db(self.DB_URL)


# testing for the users api endpoints
class TestUsersEndpoints(UserBaseTest):
   
   # tests that a user can sign up to the system
    def test_that_a_user_can_sign_up_successfully(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.signup_user1),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], 'User Registered Successfully!')


    # tests that a user can login successfully
    def test_that_a_user_can_login_successfully(self):
        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.signup_user1),
                         content_type="application/json")
        response = self.client.post("api/v2/auth/login",
                                    data=json.dumps(self.login_user1),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertTrue(result['token'])
        self.assertEqual(result["message"], "Logged in successfully")


    # tests user can login successfully
    def test_that_a_user_can_logout_successfully(self):
        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.signup_user1),
                         content_type="application/json")
        login = self.client.post("api/v2/auth/login",
                                 data=json.dumps(self.login_user1),
                                 content_type="application/json")
        user_data = json.loads(login.data.decode('utf-8'))
        token = user_data['token']
        response = self.client.post("api/v2/auth/logout",
                                    headers={'x-access-token': token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertTrue(result['status'], 200)
        self.assertEqual(result["data"], "Logged out successfully")
