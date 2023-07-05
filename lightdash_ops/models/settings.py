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

from functools import lru_cache

from pydantic import BaseSettings, Field


class LightdashOpsSettings(BaseSettings):
    """Global settings

    NOTE Pydantic enables us to parse environment variables.

    SEE https://docs.pydantic.dev/latest/usage/settings/
    """
    LIGHTDASH_URL: str = Field(default=None,
                               qdescription='Lightdash base URL',
                               env='LIGHTDASH_URL')
    LIGHTDASH_API_KEY: str = Field(default=None,
                                   qdescription='Lightdash API key',
                                   env='LIGHTDASH_API_KEY')
    LIGHTDASH_CLIENT_TIMEOUT: float = Field(default=5.0,
                                            qdescription='Lightdash base URL',
                                            env='LIGHTDASH_CLIENT_TIMEOUT')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Validate settings
        if self.LIGHTDASH_URL is None:
            raise ValueError('LIGHTDASH_URL is not set')
        if self.LIGHTDASH_API_KEY is None:
            raise ValueError('LIGHTDASH_API_KEY is not set')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Singleton
@lru_cache(maxsize=None)
def get_settings(**kwargs) -> LightdashOpsSettings:
    """Get the settings as a singleton

    SEE https://fastapi.tiangolo.com/es/advanced/settings/#creating-the-settings-only-once-with-lru_cache
    """
    return LightdashOpsSettings(**kwargs)
