import json
import unittest
from flask import Flask
from app.models.model import Redflag, User
from app import app
from app.auth.decorator import get_token, token_required, response_message
from app.database.db import Database


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db = Database()
        db.create_tables()

    def test_if_cant_get_userswithouttoken(self):
        response = self.app.get('api/v1/users')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual('please login', data['message'])

    def test_redflag(self):
        redflag = ('flag_id','user_id','description','created_by','media','location', 'status','createdOn')
        self.assertIn("id:2 senderemail:sender_email@gmail.com recieveremail:name", str(redflag))

    def test_user(self):
        user = User(1, 'abio', 'natalie', 'nats', 'talieatalia', 'abionatline@gmail.com', '0752030815','nats123','True')
        self.assertNotEqual(str(user), 'user: 11 username:talieatalia with email abionatline@gmail.com:isAdmin:true')

    def test_db(self):
        db = Database()
        self.assertTrue(db)

    def test_db_connection(self):
        db = Database()
        self.assertTrue(db.connection)

    def tearDown(self):
        db = Database()
        db.drop_tables()


if __name__ == "__main__":
    unittest.main()
