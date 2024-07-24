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

from lightdash_ops.lightdash.settings import LightdashOpsSettings


class TestLightdashOpsSettings(unittest.TestCase):

    def test_initialization_with_valid_data(self):
        settings = LightdashOpsSettings(
            LIGHTDASH_URL='https://example.com',
            LIGHTDASH_API_KEY='test_api_key',
            LIGHTDASH_CLIENT_TIMEOUT=10.0
        )
        self.assertEqual(settings.LIGHTDASH_URL, 'https://example.com')
        self.assertEqual(settings.LIGHTDASH_API_KEY, 'test_api_key')
        self.assertEqual(settings.LIGHTDASH_CLIENT_TIMEOUT, 10.0)

    # def test_initialization_without_url(self):
    #     with self.assertRaises(ValueError) as context:
    #         LightdashOpsSettings(
    #             LIGHTDASH_API_KEY='test_api_key',
    #             LIGHTDASH_CLIENT_TIMEOUT=10.0
    #         )
    #     self.assertTrue('LIGHTDASH_URL is not set' in str(context.exception))

    # def test_initialization_without_api_key(self):
    #     with self.assertRaises(ValueError) as context:
    #         LightdashOpsSettings(
    #             LIGHTDASH_URL='https://example.com',
    #             LIGHTDASH_CLIENT_TIMEOUT=10.0
    #         )
    #     self.assertTrue('LIGHTDASH_API_KEY is not set' in str(context.exception))

    # def test_get_settings_singleton(self):
    #     settings1 = get_settings(
    #         LIGHTDASH_URL='https://example.com',
    #         LIGHTDASH_API_KEY='test_api_key',
    #         LIGHTDASH_CLIENT_TIMEOUT=10.0
    #     )
    #     settings2 = get_settings()
    #     self.assertIs(settings1, settings2)
