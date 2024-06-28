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

from lightdash_ops.lightdash.v1.get_dbt_exposures import (
    GetDbtExposures, GetDbtExposuresResponse)
from lightdash_ops.lightdash.v1.list_organization_projects import \
    ListOrganizationProjects
from lightdash_ops.tests.utils import can_call_api, get_test_lightdash_client


class TestGetDbtExposures(unittest.TestCase):

    @unittest.skipIf(not can_call_api(), 'LIGHTDASH_API_KEY is not set')
    def test_get_dbt_exposures(self):
        client = get_test_lightdash_client()
        # Get all projects
        list_organization_projects = ListOrganizationProjects(client=client)
        response = list_organization_projects.request()
        # Get dbt exposures for each project
        get_dbt_exposures = GetDbtExposures(client=client)
        for project in response.projects:
            exposures_response = get_dbt_exposures.request(project_uuid=project.projectUuid)
            self.assertIsInstance(exposures_response, GetDbtExposuresResponse)
            # Test properties of the response
            for exposure in exposures_response.results.values():
                self.assertIsInstance(exposure.name, str)
                self.assertIsInstance(exposure.description, (str, type(None)))
                self.assertIsInstance(exposure.type, str)
                self.assertIsInstance(exposure.owner.name, str)
                self.assertIsInstance(exposure.owner.email, (str, type(None)))
                self.assertIsInstance(exposure.depends_on, list)
                self.assertIsInstance(exposure.url, (str, type(None)))
                self.assertIsInstance(exposure.maturity, (str, type(None)))
                self.assertIsInstance(exposure.tags, (list, type(None)))
                self.assertIsInstance(exposure.meta, (dict, type(None)))
                self.assertIsInstance(exposure.config, (dict, type(None)))
                self.assertIsInstance(exposure.created_at, (str, type(None)))
                self.assertIsInstance(exposure.updated_at, (str, type(None)))
                self.assertIsInstance(exposure.label, (str, type(None)))

    def test_from_dict(self):
        response_data = {
            'exposure_1': {
                'name': 'Sales Dashboard',
                'description': 'A dashboard showing sales metrics',
                'type': 'dashboard',
                'owner': {'name': 'Jane Doe', 'email': 'jane.doe@example.com'},
                'dependsOn': ['ref("sales_model")', 'ref("customer_model")'],
                'url': 'http://dashboard.example.com/sales',
                'maturity': 'medium',
                'tags': ['sales', 'dashboard', 'metrics'],
                'meta': {'department': 'sales', 'priority': 'high'},
                'config': {'refresh_rate': 'daily'},
                'created_at': '2023-05-10T08:30:00Z',
                'updated_at': '2023-06-15T12:45:00Z',
                'label': 'Sales Dashboard'
            }
        }

        results = GetDbtExposuresResponse.from_dict(response_data)
        exposure = results['exposure_1']
        self.assertEqual(exposure.name, 'Sales Dashboard')
        self.assertEqual(exposure.description, 'A dashboard showing sales metrics')
        self.assertEqual(exposure.type, 'dashboard')
        self.assertEqual(exposure.owner.name, 'Jane Doe')
        self.assertEqual(exposure.owner.email, 'jane.doe@example.com')
        self.assertEqual(exposure.depends_on, ['ref("sales_model")', 'ref("customer_model")'])
        self.assertEqual(exposure.url, 'http://dashboard.example.com/sales')
        self.assertEqual(exposure.maturity, 'medium')
        self.assertEqual(exposure.tags, ['sales', 'dashboard', 'metrics'])
        self.assertEqual(exposure.meta, {'department': 'sales', 'priority': 'high'})
        self.assertEqual(exposure.config, {'refresh_rate': 'daily'})
        self.assertEqual(exposure.created_at, '2023-05-10T08:30:00Z')
        self.assertEqual(exposure.updated_at, '2023-06-15T12:45:00Z')
        self.assertEqual(exposure.label, 'Sales Dashboard')
