import datetime
import json
from tests.test_base import BaseTest


class Testsflag(BaseTest):
    def test_if_can_get_redflags(self):
        response = self.app.get('api/v1/redflags')
        data = json.loads(response.data.decode())
        self.assertEqual('please login', data['message'])

    def test_redflag_request_not_json(self):
        """ Test flag content to be posted not in json format """
        request = {
                'flag_id': 1,
                'user_id': 1,
                'description':'bribery taking place in kyaliwajjara village between a driver and a police officer',
                'created_by': 'nataline',
                'media': 'photo.jpg',
                'location': 'kyaliwajjara',
                'status': '',
                'createdOn': datetime.datetime.utcnow()

        }
        result = self.app.post(
            '/api/v1/redflags',
            content_type='text/html',
            data=json.dumps(request)
        )
        data=json.loads(result.data.decode())
        self.assertEqual(result.status_code, 401)
        self.assertEqual("please login", data['message'])
