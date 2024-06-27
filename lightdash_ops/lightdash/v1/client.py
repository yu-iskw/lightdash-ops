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

import enum
from abc import ABCMeta
from typing import Any, ClassVar, Dict, Optional

import requests
from pydantic import BaseModel, Field


class RequestType(str, enum.Enum):
    """HTTP request type"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class BaseRequestModel(BaseModel, metaclass=ABCMeta):
    """Base model for request"""

    parameters: Optional[Dict[str, str]] = Field(
        default=None, description='The parameters to pass to the request'
    )
    request_body: Optional[Dict[str, Any]] = Field(
        default=None, description='The body of the request'
    )


class BaseResponseModel(BaseModel):
    """Base model for response"""

    @classmethod
    def from_response(cls, response: requests.Response) -> 'BaseResponseModel':
        try:
            results = response.json().get('results', {})
            return cls(**results)
        except Exception as e:
            raise ValueError(f'Error processing response: {response}') from e


class LightdashClient(BaseModel):
    """A client for the Lightdash API"""

    base_url: str = Field(
        ...,
        description='The base URL of the Lightdash API',
    )
    token: str = Field(..., description='The API key to use for the Lightdash API')
    timeout: int = Field(default=30, description='The timeout for the Lightdash API')

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]

    def call(
        self,
        request_type: RequestType,
        path: str,
        parameters: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = f'{self.base_url}{path}'
        response = requests.request(
            request_type.value,
            url,
            params=parameters,
            json=data,
            headers={
                'Authorization': f'ApiKey {self.token}',
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response


class BaseLightdashApiCaller(BaseModel, metaclass=ABCMeta):
    client: LightdashClient = Field(
        ..., description='The client to use for the Lightdash API'
    )
    request_type: ClassVar[RequestType] = Field(
        ..., description='The type of request to make'
    )
    path: ClassVar[str] = Field(..., description='The path to make the request to')
