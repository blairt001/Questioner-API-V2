"""Tests for the user endpoints"""
import unittest
import json

from app import create_app
from config import app_config
from app.admin.db import init_db


class ValidationsBaseTest(unittest.TestCase):
    """
    Set up the user validation tests
    """

    def setUp(self):
        """
        lets declare the variables to use on the tests
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL']
        init_db(self.DB_URL)

        self.signup_user = {"firstname": "Tony",
                            "lastname": "MIT",
                            "username": "blairtony",
                            "phoneNumber": "0715096908",
                            "email": "blairtdev@gmail.com",
                            "password": "Blairman1234",
                            "confirm_password": "Blairman1234"}

        self.login_user = {"username": "blairtony",
                           "password": "Blairman1234"}

        self.user_email1 = {"firstname": "Lionel",
                            "lastname": "Messi",
                            "username": "limesi",
                            "phoneNumber": "0715096908",
                            "email": "limesigmail.com",
                            "password": "Limesi1234",
                            "confirm_password": "Limesi1234"}

        self.user_email2 = {"firstname": "Joshua",
                            "lastname": "Ariga",
                            "username": "arigajosh",
                            "phoneNumber": "0715096908",
                            "email": "ariga@gmailcom",
                            "password": "Ariga123",
                            "confirm_password": "Ariga123"}

        self.user_password_length = {"firstname": "Codeman",
                                     "lastname": "Pragmatic",
                                     "username": "codeprag",
                                     "phoneNumber": "0715096908",
                                     "email": "codeman@gmail.com",
                                     "password": "Code",
                                     "confirm_password": "Code"}

        self.user_pass_alphabetic = {"firstname": "Codeman",
                                     "lastname": "Pragmatic",
                                     "username": "codeprag",
                                     "phoneNumber": "0715096908",
                                     "email": "codeman@gmail.com",
                                     "password": "20192019",
                                     "confirm_password": "20192019"}

        self.user_pass_capital = {"firstname": "Kenyan",
                                  "lastname": "Man",
                                  "username": "kenyaa",
                                  "phoneNumber": "0715096908",
                                  "email": "kenyan@gmail.com",
                                  "password": "blairt1234",
                                  "confirm_password": "blair1234"}

        self.user_pass_number = {"firstname": "Kenyan",
                                 "lastname": "Man",
                                 "username": "kenyaa",
                                 "phoneNumber": "0715096908",
                                 "email": "kenyan@gmail.com",
                                 "password": "Blairtony",
                                 "confirm_password": "Blairtony"}

    # clean up the tests
    def tearDown(self):
        self.app.testing = False
        init_db(self.DB_URL)


# lets now test for user validations
class TestValidations(ValidationsBaseTest):

    # tests if user enters an invalid email
    def test_user_enter_an_invalid_email1(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_email1),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Email is Invalid")

    # tests if a user enters an invalid email
    def test_user_enter_an_invalid_email2(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_email2),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Email is Invalid")

    # tests if a user uses the correct password length
    def test_correct_user_pasword_length(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_password_length),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should not be less than 8 characters or exceed 20")

    # tests if a users password contain an alphabet
    def test_user_pasword_is_alphabets(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_pass_alphabetic),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should contain a letter between a-z")

    # tests if a users password contains a capital letter
    def test_user_pasword_contains_capital(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_pass_capital),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should contain a capital letter")

    # tests if a users password contains a number
    def test_user_pasword_number(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_pass_number), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should contain a number(0-9)")

    # tests url not found
    def test_error_handler_404_url_not_found(self):
        response = self.client.post("api/v2/auth/tonyandela",
                                    data=json.dumps(self.signup_user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result['error'], 'Url not found')

    # tests method not allowed
    def test_error_handler_405_method_not_allowed(self):
        response = self.client.get("api/v2/auth/signup",
                                   data=json.dumps(self.signup_user),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 405)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result['error'], "Method not allowed")

    # tests username already used
    def test_user_username_already_exists_in_database(self):

        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.signup_user),
                         content_type="application/json")
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.signup_user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result['error'],
            "Error. 'username' 'blairtony' is already in use")
