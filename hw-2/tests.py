import json
import unittest

from flask_hw import create_app


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.flask_app = create_app()
        self.test_client = self.flask_app.test_client()

    def test_turn(self):
        response = self.test_client.get('/hello')
        assert response.status_code == 200
        assert b"HSE OneLove!" == response.data

        response = self.test_client.post('/hello')
        assert response.status_code == 405
        assert b"" == response.data

    def test_storage(self):
        response = self.test_client.post('/set',
                                         data=json.dumps(dict(key='key', value='value')),
                                         content_type='application/json')
        assert response.status_code == 200
        assert b"" == response.data

        response = self.test_client.get('/set',
                                        data=json.dumps(dict(key='key', value='value')),
                                        content_type='application/json')
        assert response.status_code == 405

        response = self.test_client.post('/set',
                                         data=json.dumps(dict(kkey='key', value='value')),
                                         content_type='application/json')
        assert response.status_code == 400

        response = self.test_client.post('/set',
                                         data=json.dumps(dict(key='key', vvalue='value')),
                                         content_type='application/json')
        assert response.status_code == 400

        response = self.test_client.get('/get/key')
        assert response.status_code == 200
        assert b'{"key": "key", "value": "value"}' == response.data

        response = self.test_client.post('/get/key')
        assert response.status_code == 405

        response = self.test_client.get('/get/kkkey')
        assert response.status_code == 404

    def test_divide(self):
        response = self.test_client.post('/divide',
                                         data=json.dumps(dict(dividend=100, divider=10)),
                                         content_type='application/json')
        assert response.status_code == 200
        assert b"10.0" == response.data

        response = self.test_client.post('/divide',
                                         data=json.dumps(dict(ddividend=100, divider=10)),
                                         content_type='application/json')
        assert response.status_code == 400

        response = self.test_client.get('/divide',
                                        data=json.dumps(dict(dividend=100, divider=10)),
                                        content_type='application/json')
        assert response.status_code == 405

        response = self.test_client.post('/divide',
                                         data=json.dumps(dict(dividend='aaa', divider=10)),
                                         content_type='application/json')
        assert response.status_code == 400


if __name__ == '__main__':
    unittest.main()
