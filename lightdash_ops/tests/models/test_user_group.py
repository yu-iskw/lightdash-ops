#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

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
