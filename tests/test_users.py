from app.database.db import Database
from app.models.model import User
from flask import Flask
import json
from app.models.model import Redflag, User
from tests.test_base import BaseTest

db = Database()


class TestAuth(BaseTest):
    def register(self, user_id, firstname,lastname,othername, username, email, phone_number, password, isAdmin):
        """
        Method to define user registration details
        """
        obj = {
            "user_id": user_id,
            "firstname": firstname,
            "lastname": lastname,
            "othername":othername,
            "username": username,
            "email": email,
            "phone_number": phone_number,
            "password": password,
            "isAdmin":"" 
        }
        return self.app.post(
            '/api/v1/auth/register',
            content_type="application/json",
            data=json.dumps(obj)
        )

    def login_user(self, email, password):
        """
        Method to define user login details
        """
        obj = {
            "email": email,
            "password": password
        }
        return self.app.post(
            '/api/v1/auth/login',
            content_type="application/json",
            data=json.dumps(obj)
        )

    def test_user_class(self):
        user = User(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','nats123','True')
        self.assertTrue(user)

    def test_details_json_format(self):
        with self.app:
            result = self.register(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','nats123','True')
            self.assertTrue(result.content_type == "application/json")

    def test_email_not_valid(self):
        """
         Test for invalid email address
         """
        register = {
            "username": "talieatalia",
            "email": "email",
            "phone_number": "0752030815",
            "password": "password",
        }
        rs = self.app.post(
            '/api/v1/auth/register',
            content_type="application/json",
            data=json.dumps(register)
        )
        data = json.loads(rs.data.decode())
        self.assertEqual(rs.status_code, 400)

    def test_short_password(self):
        """
        Test for short password
        """
        with self.app:
            result = self.register(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','na','True')
            self.assertEqual(result.status_code, 400)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'Ensure password is atleast 6 characters')

    def test_username_is_string(self):
        """
        Test username isstring
        """
        with self.app:
            result = self.register(1, 123, 3, 'nats', 'talie123', 'abionatline@gmail.com', '0752030815','nats123','True')
            self.assertEqual(result.status_code, 400)
            data = json.loads(result.data.decode())
            self.assertEqual(data['status'], 'Invalid')
            self.assertEqual(data['message'], 'firstname and lastname should be of type string')

    def test_username_empty(self):
        """
        Test username field left empty
        """
        with self.app:
            result = self.register(1, 'abio', 'natalie', 'nats','', 'abionatline@gmail.com', '0752030815','nats123','True')
            self.assertEqual(result.status_code, 400)
            data = json.loads(result.data.decode())
            self.assertEqual(data['message'], 'Firstname,lastname and username should be atleast 3 characters long')

    def test_user_data_not_json(self):
        """
        Test Content_type not application/json for sign up request
        """
        rqst = self.app.post(
            '/api/v1/auth/register',
            content_type="text",data="")

        data = json.loads(rqst.data.decode())
        self.assertEqual(rqst.status_code, 400)
        self.assertEqual(
            "Content-type must be json type", data['message'])

    def test_content_type_4_login_not_json(self):
        """
        Test Content_type not application/json for login request
        """
        rq = self.app.post(
            '/api/v1/auth/login',
            content_type="text")
        data = json.loads(rq.data.decode())
        self.assertEqual(rq.status_code, 400)
        self.assertEqual(
            "Content-type must be in json", data['message'])
        self.assertEqual(
            "Bad request", data['status'])

    def test_user_already_exist(self):
        with self.app:
            self.register(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','na','True')
            result = self.register(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','na','True')
            self.assertEqual(result.status_code, 409)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Failed')

    def test_successful_login(self):
        with self.app:
            self.register(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','na','True')
            response = self.login_user("abionatline@gmail.comm", "password")
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                "You have successfully logged in", str(res['message']))

    def test_login_credentials(self):
        with self.app:
            self.register(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','na','True')
            resp = self.login_user("abionatline@gmail.com", "wrongpassw")
            res = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(res['status'], 'Failed')
            self.assertEqual(
                'email or password is invalid', str(res['message']))