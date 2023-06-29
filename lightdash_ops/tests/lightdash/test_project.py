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

from lightdash_ops.lightdash.organization import get_projects
from lightdash_ops.lightdash.project import get_project_members
from lightdash_ops.tests.utils import get_test_client, has_lightdash_api_key


class TestLightdashOrganization(unittest.TestCase):

    def setUp(self) -> None:
        self.client = get_test_client()

    @unittest.skipIf(not has_lightdash_api_key(), 'LIGHTDASH_API_KEY environment variable not set')
    def test_get_project_members(self):
        projects = get_projects(client=self.client)
        for project in projects:
            members = get_project_members(client=self.client, project_uuid=project.project_uuid)
            if len(members) > 0:
                self.assertIsNotNone(members[0].email)
                self.assertIsNotNone(members[0].role)
