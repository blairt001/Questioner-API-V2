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

        self.signup_user1 = {"firstname":"Tony",
                             "lastname": "Blair",
                             "phoneNumber":"0715096908",
                             "username":"blairtony",
                             "email":"blairt37.dev@gmail.com",
                             "password": "Blairman1234",
                             "confirmpassword":"Blairman1234"}

        self.signup_user2 = {"firstname":"Lionel",
                             "lastname": "Messi",
                             "phoneNumber":"0715096908",
                             "username":"limesi",
                             "email":"limesi@gmail.com",
                             "password": "Limesi1234",
                             "confirmpassword":"Limesi123"}

        self.signup_user3 = {"firstname":"Joshua",
                             "lastname": "Ariga",
                             "username":"arigajosh",
                             "email":"ariga@gmail.com",
                             "password": "Ariga123",
                             "confirmpassword":"Ariga123"}

        self.signup_user4 = {"firstname":"Codeman",
                             "lastname": "Pragmatic",
                             "phoneNumber":"0723456789",
                             "username":"codeprag",
                             "email":"codeman@gmail.com",
                             "password": "Cod1",
                             "confirmpassword":"Cod1"}

        self.signup_user5 = {"firstname":"Codeman",
                             "lastname": "Pragmatic",
                             "phoneNumber":"0723456789",
                             "username":"codeprag",
                             "email":"codeman@gmail.com",
                             "password": "Codedsdscfsdfsfsfhchdfgvdyvhgsdvghsd",
                             "confirmpassword":"Codedsdscfsdfsfsfhchdfgvdyvhgsdvghsd"}


        self.signup_user6 = {"firstname":"Kenyan",
                             "lastname": "Man",
                             "phoneNumber":"0715096908",
                             "username":"kenyaa",
                             "email":"kenyan@gmail",
                             "password": "@Mitcoder1",
                             "confirmpassword":"@Mitcoder1"}

        self.login_user1 = {"username":"blairtony",
                            "password":"Blairman1234"}

        self.login_user2 = {"username":"limesi",
                            "password":"Limesi1234"}

        self.login_user3 = {"username":"kenyaa",
                            "password":"@Mitcoder1"}

        token = ''
    #clean up the tests
    def tearDown(self):
        self.app.testing = False
        init_db(self.DB_URL)

#testing for the users endpoints
class TestUsersEndpoints(UserBaseTest):

    def test_user_wrong_json_keys(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.signup_user3),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result['error'],
            'Should be firstname, lastname, username, email, phoneNumber, password and confirmpassword')

    def test_user_can_sign_up(self):
        """
        Tests to confirm a user signup successfully
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.signup_user1), content_type = "application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], 'User Registered Successfully!')
    