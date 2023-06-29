import unittest

from pydantic import EmailStr

from lightdash_ops.models.base_user import LightdashUser


class TestLightdashUser(unittest.TestCase):

    def test_json_1(self):
        user = LightdashUser(email=EmailStr('test@example.com'))
        expected = '{"email": "test@example.com", "uuid": null}'
        self.assertEqual(expected, user.json())

    def test_json_2(self):
        user = LightdashUser(email=EmailStr('test@example.com'), uuid='dummy-uuid')
        expected = '{"email": "test@example.com", "uuid": "dummy-uuid"}'
        self.assertEqual(expected, user.json())
