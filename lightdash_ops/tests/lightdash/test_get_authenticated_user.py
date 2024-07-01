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

from lightdash_ops.lightdash.v1.get_authenticated_user import (
    GetAuthenticatedUser, GetAuthenticatedUserApiV1Response)
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetAuthenticatedUser(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_authenticated_user(self):
        client = get_test_lightdash_client()
        get_authenticated_user = GetAuthenticatedUser(client=client)
        response = get_authenticated_user.request()
        self.assertIsInstance(response, GetAuthenticatedUserApiV1Response)
        # Test properties of the response
        self.assertIsInstance(response.userUuid, str)
        self.assertIsInstance(response.email, str)
        self.assertIsInstance(response.firstName, str)
        self.assertIsInstance(response.lastName, str)
        self.assertIsInstance(response.organizationUuid, (str, type(None)))
        self.assertIsInstance(response.organizationName, (str, type(None)))
        self.assertIsInstance(response.organizationCreatedAt, (str, type(None)))
        self.assertIsInstance(response.isTrackingAnonymized, bool)
        self.assertIsInstance(response.isMarketingOptedIn, bool)
        self.assertIsInstance(response.isSetupComplete, bool)
        self.assertIsInstance(response.role, (str, type(None)))
        self.assertIsInstance(response.isActive, bool)
        self.assertIsInstance(response.additionalProperties, dict)

    def test_from_response(self):
        response_data = {
            'userUuid': '1234-5678-91011',
            'email': 'test@example.com',
            'firstName': 'John',
            'lastName': 'Doe',
            'organizationUuid': 'abcd-efgh-ijkl',
            'organizationName': 'Test Organization',
            'organizationCreatedAt': '2023-01-01T00:00:00Z',
            'isTrackingAnonymized': True,
            'isMarketingOptedIn': False,
            'isSetupComplete': True,
            'role': 'admin',
            'isActive': True,
            'additionalProperties': {},
        }

        response = GetAuthenticatedUserApiV1Response(**response_data)
        self.assertEqual(response.userUuid, '1234-5678-91011')
        self.assertEqual(response.email, 'test@example.com')
        self.assertEqual(response.firstName, 'John')
        self.assertEqual(response.lastName, 'Doe')
        self.assertEqual(response.organizationUuid, 'abcd-efgh-ijkl')
        self.assertEqual(response.organizationName, 'Test Organization')
        self.assertEqual(response.organizationCreatedAt, '2023-01-01T00:00:00Z')
        self.assertTrue(response.isTrackingAnonymized)
        self.assertFalse(response.isMarketingOptedIn)
        self.assertTrue(response.isSetupComplete)
        self.assertEqual(response.role, 'admin')
        self.assertTrue(response.isActive)
        self.assertEqual(response.additionalProperties, {})
