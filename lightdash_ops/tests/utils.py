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
from typing import Optional

from lightdash_ops.lightdash.v1.client import LightdashClient


def get_lightdash_api_key() -> Optional[str]:
    """Get the LIGHTDASH_API_KEY environment variable"""
    return os.getenv('LIGHTDASH_API_KEY')


def get_base_url() -> str:
    """Get the base URL for the Lightdash API"""
    return os.getenv('LIGHTDASH_URL', 'https://app.lightdash.cloud')


def can_call_api() -> bool:
    """Check if unit tests with actual API calls can be executed.

    Those environment variables are needed to set to call the Lightdash API:
    - LIGHTDASH_API_KEY
    - LIGHTDASH_URL
    """
    if get_lightdash_api_key() is not None and get_base_url() is not None:
        return True
    return False


def has_lightdash_project_uuid() -> bool:
    """Check if APi key and project UUID environment variables are set"""
    if (
        os.getenv('LIGHTDASH_API_KEY') is not None
        and os.getenv('LIGHTDASH_PROJECT_UUID') is not None
    ):
        return True
    return False


def get_lightdash_project_uuid() -> Optional[str]:
    """Get the LIGHTDASH_PROJECT_UUID environment variable"""
    return os.getenv('LIGHTDASH_PROJECT_UUID')


def get_test_lightdash_client() -> LightdashClient:
    """Get a test client for the Lightdash API"""
    return LightdashClient(
        token=get_lightdash_api_key(),
        base_url=get_base_url(),
    )
