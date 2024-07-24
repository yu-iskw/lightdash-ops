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

from lightdash_ops.lightdash.v1.get_project import (GetProject,
                                                    GetProjectApiV1Response)
from lightdash_ops.lightdash.v1.list_organization_projects import \
    ListOrganizationProjects
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetProject(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_project(self):
        client = get_test_lightdash_client()
        # Get all projects
        list_organization_projects = ListOrganizationProjects(client=client)
        response = list_organization_projects.request()
        # Get each project
        get_project = GetProject(client=client)
        for project in response.projects:
            response = get_project.request(projectUuid=project.projectUuid)
            self.assertIsInstance(response, GetProjectApiV1Response)
            # Test properties of the response
            self.assertIsInstance(response.dbtVersion, (str, type(None)))
            self.assertIsInstance(response.upstreamProjectUuid, (str, type(None)))
            self.assertIsInstance(response.pinnedListUuid, (str, type(None)))
            self.assertIsInstance(response.warehouseConnection, (dict, type(None)))
            self.assertIsInstance(response.dbtConnection, (dict, type(None)))
            self.assertIsInstance(response.type, str)
            self.assertIsInstance(response.name, str)
            self.assertIsInstance(response.projectUuid, str)
            self.assertIsInstance(response.organizationUuid, str)

    def test_from_response(self):
        response_data = {
            'dbtVersion': '0.20.0',
            'upstreamProjectUuid': '5678-91011-1234',
            'pinnedListUuid': '91011-1234-5678',
            'warehouseConnection': {'type': 'bigquery'},
            'dbtConnection': {'type': 'dbt-cloud'},
            'type': 'analytics',
            'name': 'Test Project',
            'projectUuid': 'test-project-uuid',
            'organizationUuid': 'abcd-efgh-ijkl',
        }

        response = GetProjectApiV1Response(**response_data)
        self.assertEqual(response.dbtVersion, '0.20.0')
        self.assertEqual(response.upstreamProjectUuid, '5678-91011-1234')
        self.assertEqual(response.pinnedListUuid, '91011-1234-5678')
        self.assertEqual(response.warehouseConnection, {'type': 'bigquery'})
        self.assertEqual(response.dbtConnection, {'type': 'dbt-cloud'})
        self.assertEqual(response.type, 'analytics')
        self.assertEqual(response.name, 'Test Project')
        self.assertEqual(response.projectUuid, 'test-project-uuid')
        self.assertEqual(response.organizationUuid, 'abcd-efgh-ijkl')
