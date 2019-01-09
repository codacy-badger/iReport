import unittest
from test_base import BaseTestCase
# from flask import app
from flask import json

class Useroperations(BaseTestCase):
   #  client = app.testbase()
    user = {
            "firstname":"Abio",
            "secondname": "Nataline",
            "username": "abbie",
            "email": "abionatline@gmail.com",
            "password": "nats123456"
           }

    users = {
        'username': "username",
        'password': "password"
        }

    def test_register_successfully(self):
       
       response = self.post('/api/v1/register', data=json.dumps(self.user), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual('Account created successfully', data['message'])
       self.assertEqual(201, response.status_code)

    def test_name_missing(self):
       user2 = self.user
       del user2['username']
       response = self.client.post('/api/v1/register', data=json.dumps(user2), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual("field can't be blank", data['message'])
       self.assertEqual(400, response.status_code)

    def test_email_missing(self):
       user2 = self.user
       del user2['email']
       response = self.client.post('/api/v1/register', data=json.dumps(user2), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual("field can't be blank", data['message'])
       self.assertEqual(400, response.status_code)

    def test__password_missing(self):
       user2 = self.user
       del user2['password']
       response = self.client.post('/api/v1/register', data=json.dumps(user2), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual("field can't be blank", data['message'])
       self.assertEqual(400, response.status_code)

    def test__login_successfully(self):
       
       response = self.client.post('/api/v1/login', data=json.dumps(self.users), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual("login successful", data['message'])
       self.assertEqual(200, response.status_code)

    def test__username(self):
       users2 = self.users
       del users2['password']
       response = self.client.post('/api/v1/login', data=json.dumps(users2), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual("field can't be blank", data['message'])
       self.assertEqual(400, response.status_code)

    def test__password(self):
       user2 = self.user
       del user2['password']
       response = self.client.post('/api/v1/login', data=json.dumps(user2), content_type='application/json')
       data = json.loads(response.data.decode())
       self.assertEqual("field can't be blank", data['message'])
       self.assertEqual(400, response.status_code)


class Redflag(BaseTestCase):
   flag = {
       'location': "Bwaise",
       'type': "bribery",
       'description': "a driver bribing a traffic police officer",
       'media': "photo.jpg"
    }
    
   def test_redfag_created(self):

      response = self.client.post('/api/v1/regflag', data=json.dumps(self.flag), content_type='application/json')
      data = json.loads(response.data.decode())
      print(data)
      self.assertEqual('Redflag created', data['message'])
      self.assertEqual(201, response.status_code)

     
    


if __name__ == '__main__':
   unittest.main()