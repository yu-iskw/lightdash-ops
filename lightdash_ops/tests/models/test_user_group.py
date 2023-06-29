import json
import unittest

from pydantic import EmailStr

from lightdash_ops.models.user_group import GroupMember, UserGroup


class TestUserGroup(unittest.TestCase):

    def test_json_1(self):
        group = UserGroup(name='test group')
        expected = {
            'created_at': None,
            'enabled': True,
            'members': [],
            'name': 'test group',
            'organization_uuid': None,
            'uuid': None,
        }
        self.assertDictEqual(expected, json.loads(group.json()))

    def test_json_2(self):
        group = UserGroup(
            enabled=False,
            name='test group',
            uuid='dummy-uuid',
            members=[
                GroupMember(email=EmailStr('test@example.com')),
                GroupMember(
                    email=EmailStr('test2@example.com'),
                    uuid='dummy-uuid',
                ),
            ],
        )
        expected = {
            'created_at': None,
            'enabled': False,
            'members': [
                {'email': 'test@example.com', 'uuid': None},
                {'email': 'test2@example.com', 'uuid': 'dummy-uuid'},
            ],
            'name': 'test group',
            'organization_uuid': None,
            'uuid': 'dummy-uuid'
        }
        self.assertDictEqual(expected, json.loads(group.json()))


class TestGroupMember(unittest.TestCase):

    def test_valid_new(self):
        # pylint: disable=invalid-name
        # Create the project member
        email = 'test@example.com'
        group_member = GroupMember(email=EmailStr(email))
        self.assertEqual(group_member.email, email)

    def test_json_1(self):
        group_member = GroupMember(email=EmailStr('test@example.com'))
        expected = {'email': 'test@example.com', 'uuid': None}
        self.assertDictEqual(expected, json.loads(group_member.json()))

    def test_json_2(self):
        # pylint: disable=invalid-name

        # Test
        group_member = GroupMember(
            email=EmailStr('test@example.com'),
            uuid='dummy-uuid',
        )
        expected = {'email': 'test@example.com', 'uuid': 'dummy-uuid'}
        self.assertDictEqual(expected, json.loads(group_member.json()))
