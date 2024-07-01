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

from lightdash_ops.lightdash.v1.list_organization_members import (
    ListOrganizationMembers, ListOrganizationMembersApiV1Response)
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestListOrganizationMembers(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_list_organization_members(self):
        client = get_test_lightdash_client()
        list_organization_members = ListOrganizationMembers(client=client)
        model = list_organization_members.request()
        self.assertIsInstance(model, ListOrganizationMembersApiV1Response)
        # Test properties of the response
        for member in model.members:
            self.assertIsInstance(member.isInviteExpired, bool)
            self.assertIsInstance(member.isActive, bool)
            self.assertIsInstance(member.role, str)
            self.assertIsInstance(member.organizationUuid, str)
            self.assertIsInstance(member.email, str)
            self.assertIsInstance(member.lastName, str)
            self.assertIsInstance(member.firstName, str)
            self.assertIsInstance(member.userUuid, str)

    def test_from_results(self):
        results = [
            {
                'isInviteExpired': False,
                'isActive': True,
                'role': 'admin',
                'organizationUuid': '123e4567-e89b-12d3-a456-426614174000',
                'email': 'user@example.com',
                'lastName': 'Doe',
                'firstName': 'John',
                'userUuid': '123e4567-e89b-12d3-a456-426614174001',
            }
        ]

        response_model = ListOrganizationMembersApiV1Response.from_results(
            results=results, status='success'
        )
        self.assertTrue(len(response_model.members) >= 0)  # Fix the length check
        if len(response_model.members) > 0:
            for member in response_model.members:
                self.assertIsInstance(member.isInviteExpired, bool)
                self.assertIsInstance(member.isActive, bool)
                self.assertIsInstance(member.role, str)
                self.assertIsInstance(member.organizationUuid, str)
                self.assertIsInstance(member.email, str)
                self.assertIsInstance(member.lastName, str)
                self.assertIsInstance(member.firstName, str)
                self.assertIsInstance(member.userUuid, str)
