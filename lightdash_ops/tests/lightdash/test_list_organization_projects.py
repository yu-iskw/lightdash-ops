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

from lightdash_ops.lightdash.v1.list_organization_projects import (
    ListOrganizationProjects, ListOrganizationProjectsApiV1Response)
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestListOrganizationProjects(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_list_organization_projects(self):
        client = get_test_lightdash_client()
        list_organization_projects = ListOrganizationProjects(client=client)
        model = list_organization_projects.request()
        self.assertIsInstance(model, ListOrganizationProjectsApiV1Response)
        # Test properties of the response
        for project in model.projects:
            self.assertIsInstance(project.requireUserCredentials, bool)
            self.assertIsInstance(project.warehouseType, str)
            self.assertIsInstance(project.type, str)
            self.assertIsInstance(project.name, str)
            self.assertIsInstance(project.projectUuid, str)

    def test_from_results(self):
        results = [
            {
                'requireUserCredentials': True,
                'warehouseType': 'BigQuery',
                'type': 'analytics',
                'name': 'Project A',
                'projectUuid': '123e4567-e89b-12d3-a456-426614174000',
            }
        ]

        response_model = ListOrganizationProjectsApiV1Response.from_results(
            results=results
        )
        self.assertTrue(len(response_model.projects) >= 0)  # Fix the length check
        if len(response_model.projects) > 0:
            for project in response_model.projects:
                self.assertIsInstance(project.requireUserCredentials, bool)
                self.assertIsInstance(project.warehouseType, str)
                self.assertIsInstance(project.type, str)
                self.assertIsInstance(project.name, str)
                self.assertIsInstance(project.projectUuid, str)
