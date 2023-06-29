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

import os
import unittest

from lightdash_ops.models.settings import LightdashOpsSettings


class TestManagerSettings(unittest.TestCase):

    def test_set_by_env_vars(self):
        # Configure the settings by env vars
        os.environ['LIGHTDASH_BASE_URL'] = 'http://localhost:8000'
        os.environ['LIGHTDASH_CLIENT_TIMEOUT'] = '1'

        # Create the settings
        settings = LightdashOpsSettings()
        self.assertEqual(settings.LIGHTDASH_BASE_URL, 'http://localhost:8000')
        self.assertEqual(settings.LIGHTDASH_CLIENT_TIMEOUT, 1)
