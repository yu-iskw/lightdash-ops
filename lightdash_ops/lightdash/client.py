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

from lightdash_client import AuthenticatedClient


def get_lightdash_client(
        api_key: str,
        timeout: float = 5.0,
        base_url='https://app.lightdash.cloud') -> AuthenticatedClient:
    """Get a test client for the Lightdash API

    The function is used to skip tests that require a valid API key.
    """
    client = AuthenticatedClient(base_url=base_url, token=api_key, timeout=timeout)
    return client  # type: ignore
