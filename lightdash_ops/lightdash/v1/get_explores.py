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

from typing import ClassVar, List, Optional

import requests
from pydantic import BaseModel, Field

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               BaseResponseModel, RequestType)


# pylint: disable=invalid-name
class GetExploresApiV1Response(BaseResponseModel):
    class Explore(BaseModel):
        class Config:
            extra = 'allow'

        name: str = Field(..., description='The name of the explore')
        label: Optional[str] = Field(None, description='The label of the explore')
        groupLabel: Optional[str] = Field(
            None, description='The group label of the explore'
        )
        tags: Optional[List[str]] = Field(
            default_factory=list, description='The tags associated with the explore'
        )
        databaseName: str = Field(..., description='The database name of the explore')
        schemaName: str = Field(..., description='The schema name of the explore')
        description: Optional[str] = Field(
            None, description='The description of the explore'
        )
        errors: Optional[List[dict]] = Field(
            default_factory=list, description='The errors associated with the explore'
        )

    explores: List[Explore] = Field(
        ..., default_factory=list, description='List of explores'
    )
    status: str = Field(..., description='The status of the response')

    @classmethod
    def from_response(cls, response: requests.Response) -> 'GetExploresApiV1Response':
        results = response.json().get('results', [])
        status = response.json().get('status', 'unknown')
        return cls.from_results(results, status)

    @classmethod
    def from_results(cls, results: dict, status: str) -> 'GetExploresApiV1Response':
        for explore in results:
            try:
                cls.Explore(**explore)
            except Exception as e:
                raise ValueError(f'Failed to parse explore: {explore}') from e
        explores = [cls.Explore(**explore) for explore in results]
        return cls(explores=explores, status=status)


class GetExplores(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}/explores'

    def request(self, projectUuid: str) -> GetExploresApiV1Response:
        response = self.client.call(
            request_type=self.__class__.request_type,
            path=self.__class__.path.format(projectUuid=projectUuid),
        )
        return GetExploresApiV1Response.from_response(response=response)
