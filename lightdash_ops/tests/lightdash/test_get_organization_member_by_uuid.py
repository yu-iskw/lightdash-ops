# Copyright 2024 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest

from lightdash_ops.lightdash.v1.get_organization_member_by_uuid import (
    GetOrganizationMemberByUuid, GetOrganizationMemberByUuidApiV1Response)
from lightdash_ops.lightdash.v1.list_organization_members import \
    ListOrganizationMembers
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetOrganizationMemberByUuid(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_organization_member_by_uuid(self):
        client = get_test_lightdash_client()
        # Get organization members
        list_organization_members = ListOrganizationMembers(client=client)
        organization_members_response = list_organization_members.request()

        get_organization_member_by_uuid = GetOrganizationMemberByUuid(client=client)
        for organization_member in organization_members_response.members[:5]:
            response = get_organization_member_by_uuid.request(
                user_uuid=organization_member.userUuid
            )
            self.assertIsInstance(response, GetOrganizationMemberByUuidApiV1Response)
            # Test properties of the response
            self.assertIsInstance(response.isInviteExpired, (bool, type(None)))
            self.assertIsInstance(response.isActive, bool)
            self.assertIsInstance(response.role, str)
            self.assertIsInstance(response.organizationUuid, str)
            self.assertIsInstance(response.email, str)
            self.assertIsInstance(response.lastName, str)
            self.assertIsInstance(response.firstName, str)
            self.assertIsInstance(response.userUuid, str)

    def test_from_response(self):
        response_data = {
            'isInviteExpired': False,
            'isActive': True,
            'role': 'admin',
            'organizationUuid': 'abcd-efgh-ijkl',
            'email': 'user@example.com',
            'lastName': 'Doe',
            'firstName': 'John',
            'userUuid': 'test-user-uuid',
        }

        response = GetOrganizationMemberByUuidApiV1Response(**response_data)
        self.assertEqual(response.isInviteExpired, False)
        self.assertEqual(response.isActive, True)
        self.assertEqual(response.role, 'admin')
        self.assertEqual(response.organizationUuid, 'abcd-efgh-ijkl')
        self.assertEqual(response.email, 'user@example.com')
        self.assertEqual(response.lastName, 'Doe')
        self.assertEqual(response.firstName, 'John')
        self.assertEqual(response.userUuid, 'test-user-uuid')
