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
class ListOrganizationMembersApiV1Response(BaseResponseModel):
    class Member(BaseModel):
        isInviteExpired: bool = Field(..., description='Whether the invite is expired')
        isActive: bool = Field(..., description='Whether the member is active')
        role: str = Field(..., description='The role of the member')
        organizationUuid: str = Field(
            ..., description='The unique identifier of the organization'
        )
        email: str = Field(..., description='The email of the member')
        lastName: str = Field(..., description='The last name of the member')
        firstName: str = Field(..., description='The first name of the member')
        userUuid: str = Field(..., description='The unique identifier of the user')

    members: List[Member] = Field(
        ..., default_factory=list, description='List of members'
    )
    status: str = Field(..., description='The status of the response')

    @classmethod
    def from_response(
        cls, response: requests.Response
    ) -> 'ListOrganizationMembersApiV1Response':
        results = response.json().get('results', [])
        status = response.json().get('status', 'unknown')
        return cls.from_results(results, status)

    @classmethod
    def from_results(
        cls, results: dict, status: str
    ) -> 'ListOrganizationMembersApiV1Response':
        members = [cls.Member(**member) for member in results]
        return cls(members=members, status=status)


class ListOrganizationMembers(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/org/users'

    def request(self) -> ListOrganizationMembersApiV1Response:
        response = self.client.call(
            request_type=self.__class__.request_type,
            path=self.__class__.path,
        )
        return ListOrganizationMembersApiV1Response.from_response(response=response)
