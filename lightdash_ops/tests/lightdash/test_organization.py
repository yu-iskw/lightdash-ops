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

from lightdash_ops.lightdash.organization import (get_organization_members,
                                                  get_projects)
from lightdash_ops.tests.utils import get_test_client, has_lightdash_api_key


class TestLightdashOrganization(unittest.TestCase):

    def setUp(self) -> None:
        self.client = get_test_client()

    @unittest.skipIf(not has_lightdash_api_key(), 'LIGHTDASH_API_KEY environment variable not set')
    def test_get_projects(self):
        projects = get_projects(client=self.client)
        if len(projects) > 0:
            self.assertIsNotNone(projects[0].type)
            self.assertIsNotNone(projects[0].name)
            self.assertIsNotNone(projects[0].project_uuid)

    @unittest.skipIf(not has_lightdash_api_key(), 'LIGHTDASH_API_KEY environment variable not set')
    def test_get_members(self):
        members = get_organization_members(client=self.client)
        if len(members) > 0:
            self.assertTrue(members[0].email is not None)
            self.assertTrue(members[0].user_uuid is not None)
            self.assertTrue(members[0].role is not None)
