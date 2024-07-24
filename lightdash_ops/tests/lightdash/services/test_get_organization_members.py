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

import unittest

from lightdash_ops.lightdash.models.organization import OrganizationMember
from lightdash_ops.lightdash.services.get_organization_members import \
    GetOrganizationMembersService
from lightdash_ops.lightdash.v1.list_organization_members import \
    ListOrganizationMembersApiV1Response
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetOrganizationMembersService(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_all_members(self):
        client = get_test_lightdash_client()
        service = GetOrganizationMembersService(client=client, members=[])
        members = service.get_all_members(page_size=10)

        self.assertIsInstance(members, list)
        for member in members:
            self.assertIsInstance(member, OrganizationMember)
            self.assertIsInstance(member.user_uuid, str)
            self.assertIsInstance(member.email, str)
            self.assertIsInstance(member.role, str)
            self.assertIsInstance(member.is_active, bool)

    def test_from_results(self):
        response_data = {
            'data': [
                {
                    'userUuid': '1234-5678-91011',
                    'email': 'test1@example.com',
                    'role': 'admin',
                    'isActive': True,
                    'isInviteExpired': False,
                    'organizationUuid': 'org-uuid-1',
                    'lastName': 'Doe',
                    'firstName': 'John',
                },
                {
                    'userUuid': '2234-5678-91011',
                    'email': 'test2@example.com',
                    'role': 'viewer',
                    'isActive': False,
                    'isInviteExpired': False,
                    'organizationUuid': 'org-uuid-2',
                    'lastName': 'Smith',
                    'firstName': 'Jane',
                },
            ]
        }

        response = ListOrganizationMembersApiV1Response.from_results(
            response_data, status='ok'
        )
        self.assertEqual(len(response.members), 2)
        self.assertEqual(response.members[0].userUuid, '1234-5678-91011')
        self.assertEqual(response.members[0].email, 'test1@example.com')
        self.assertEqual(response.members[0].role, 'admin')
        self.assertTrue(response.members[0].isActive)
        self.assertEqual(response.members[1].userUuid, '2234-5678-91011')
        self.assertEqual(response.members[1].email, 'test2@example.com')
        self.assertEqual(response.members[1].role, 'viewer')
        self.assertFalse(response.members[1].isActive)


if __name__ == '__main__':
    unittest.main()
