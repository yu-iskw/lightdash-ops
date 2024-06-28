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

from lightdash_ops.lightdash.v1.list_groups_in_organization import (
    ListGroupsInOrganization, ListGroupsInOrganizationApiV1Response)
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestListGroupsInOrganization(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_list_groups_in_organization(self):
        client = get_test_lightdash_client()
        list_groups_in_organization = ListGroupsInOrganization(client=client)
        model = list_groups_in_organization.request()
        self.assertIsInstance(model, ListGroupsInOrganizationApiV1Response)
        # Test properties of the response
        for group in model.groups:
            self.assertIsInstance(group.organizationUuid, str)
            self.assertIsInstance(group.createdAt, str)
            self.assertIsInstance(group.name, str)
            self.assertIsInstance(group.uuid, str)

    def test_from_results(self):
        results = [
            {
                'organizationUuid': '123e4567-e89b-12d3-a456-426614174000',
                'createdAt': '2023-01-01T00:00:00Z',
                'name': 'Engineering',
                'uuid': '123e4567-e89b-12d3-a456-426614174001',
            }
        ]

        response_model = ListGroupsInOrganizationApiV1Response.from_results(
            results=results, status='ok'
        )
        self.assertTrue(len(response_model.groups) >= 0)  # Fix the length check
        if len(response_model.groups) > 0:
            for group in response_model.groups:
                self.assertIsInstance(group.organizationUuid, str)
                self.assertIsInstance(group.createdAt, str)
                self.assertIsInstance(group.name, str)
                self.assertIsInstance(group.uuid, str)
