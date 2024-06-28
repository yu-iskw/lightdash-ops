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

from typing import ClassVar, List

import requests
from pydantic import BaseModel, Field

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               BaseResponseModel, RequestType)


# pylint: disable=invalid-name
class ListGroupsInOrganizationApiV1Response(BaseResponseModel):
    class Group(BaseModel):
        organizationUuid: str = Field(
            ..., description='The unique identifier of the organization'
        )
        createdAt: str = Field(..., description='The creation date of the group')
        name: str = Field(..., description='The name of the group')
        uuid: str = Field(..., description='The unique identifier of the group')

    groups: List[Group] = Field(..., default_factory=list, description='List of groups')
    status: str = Field(..., description='The status of the response')

    @classmethod
    def from_response(
        cls, response: requests.Response
    ) -> 'ListGroupsInOrganizationApiV1Response':
        results = response.json().get('results', [])
        status = response.json().get('status', 'unknown')
        return cls.from_results(results, status)

    @classmethod
    def from_results(
        cls, results: dict, status: str
    ) -> 'ListGroupsInOrganizationApiV1Response':
        groups = [cls.Group(**group) for group in results]
        return cls(groups=groups, status=status)


class ListGroupsInOrganization(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/org/groups'

    def request(self) -> ListGroupsInOrganizationApiV1Response:
        response = self.client.call(
            request_type=self.__class__.request_type,
            path=self.__class__.path,
        )
        return ListGroupsInOrganizationApiV1Response.from_response(response=response)
