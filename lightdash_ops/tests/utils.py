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

from lightdash_client import AuthenticatedClient


def has_lightdash_api_key() -> bool:
    """Check if the LIGHTDASH_API_KEY environment variable is set

    The function is used to skip tests that require a valid API key.
    """
    if os.getenv('LIGHTDASH_API_KEY') is not None:
        return True
    return False


def has_lightdash_project_uuid() -> bool:
    """Check if APi key and project UUID environment variables are set"""
    if (os.getenv('LIGHTDASH_API_KEY') is not None
            and os.getenv('LIGHTDASH_PROJECT_UUID') is not None):
        return True
    return False


def get_lightdash_project_uuid() -> Optional[str]:
    """Get the LIGHTDASH_PROJECT_UUID environment variable"""
    return os.getenv('LIGHTDASH_PROJECT_UUID')


def get_test_client(base_url='https://app.lightdash.cloud',
                    api_key: str = os.getenv('LIGHTDASH_API_KEY', '')):
    """Get a test client for the Lightdash API

    The function is used to skip tests that require a valid API key.
    """
    client = AuthenticatedClient(base_url=base_url, token=api_key)
    return client
