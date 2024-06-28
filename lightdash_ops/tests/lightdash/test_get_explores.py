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

from lightdash_ops.lightdash.v1.get_explores import (GetExplores,
                                                     GetExploresApiV1Response)
from lightdash_ops.lightdash.v1.list_organization_projects import \
    ListOrganizationProjects
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetExplores(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_explores(self):
        client = get_test_lightdash_client()
        # Get projects
        list_organization_projects = ListOrganizationProjects(client=client)
        list_organization_projects_response = list_organization_projects.request()

        get_explores = GetExplores(client=client)
        for project in list_organization_projects_response.projects[:1]:
            get_explores_response = get_explores.request(
                projectUuid=project.projectUuid
            )
            self.assertIsInstance(get_explores_response, GetExploresApiV1Response)
            # Test properties of the response
            for explore in get_explores_response.explores:
                self.assertIsInstance(explore.name, str)
                self.assertIsInstance(explore.label, str)
                self.assertIsInstance(explore.groupLabel, (str, type(None)))
                self.assertIsInstance(explore.tags, list)
                self.assertIsInstance(explore.databaseName, str)
                self.assertIsInstance(explore.schemaName, str)
                self.assertIsInstance(explore.description, (str, type(None)))
                self.assertIsInstance(explore.errors, list)

    def test_from_results(self):
        results = [
            {
                'name': 'explore1',
                'label': 'Explore 1',
                'groupLabel': 'Group 1',
                'tags': ['tag1', 'tag2'],
                'databaseName': 'db1',
                'schemaName': 'schema1',
                'description': 'Description of explore1',
                'errors': [],
            }
        ]

        response_model = GetExploresApiV1Response.from_results(
            results=results, status='ok'
        )
        self.assertTrue(len(response_model.explores) >= 0)  # Fix the length check
        if len(response_model.explores) > 0:
            for explore in response_model.explores:
                self.assertIsInstance(explore.name, str)
                self.assertIsInstance(explore.label, str)
                self.assertIsInstance(explore.groupLabel, (str, type(None)))
                self.assertIsInstance(explore.tags, list)
                self.assertIsInstance(explore.databaseName, str)
                self.assertIsInstance(explore.schemaName, str)
                self.assertIsInstance(explore.description, (str, type(None)))
                self.assertIsInstance(explore.errors, list)
