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

from lightdash_ops.lightdash.v1.get_my_organization import (
    GetOrganization, GetOrganizationApiV1Response)
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetMyOrganization(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_my_organization(self):
        client = get_test_lightdash_client()
        get_organization = GetOrganization(client=client)
        response = get_organization.request()
        self.assertIsInstance(response, GetOrganizationApiV1Response)
        # Test properties of the response
        self.assertIsInstance(response.defaultProjectUuid, (str, type(None)))
        self.assertIsInstance(response.needsProject, (bool, type(None)))
        self.assertIsInstance(response.chartColors, (list, type(None)))
        self.assertIsInstance(response.name, str)
        self.assertIsInstance(response.organizationUuid, str)

    def test_from_response(self):
        response_data = {
            'defaultProjectUuid': '1234-5678-91011',
            'needsProject': True,
            'chartColors': ['#FFFFFF', '#000000'],
            'name': 'Test Organization',
            'organizationUuid': 'abcd-efgh-ijkl',
        }

        response = GetOrganizationApiV1Response(**response_data)
        self.assertEqual(response.defaultProjectUuid, '1234-5678-91011')
        self.assertTrue(response.needsProject)
        self.assertEqual(response.chartColors, ['#FFFFFF', '#000000'])
        self.assertEqual(response.name, 'Test Organization')
        self.assertEqual(response.organizationUuid, 'abcd-efgh-ijkl')
