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
from typing_extensions import override

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               BaseResponseModel, RequestType)


# pylint: disable=invalid-name
class CreateSpaceInProjectApiV1Response(BaseResponseModel):
    class GroupAccess(BaseModel):
        spaceRole: str = Field(..., description='Role in the space')
        groupName: str = Field(..., description='Name of the group')
        groupUuid: str = Field(..., description='UUID of the group')

    class Access(BaseModel):
        inheritedFrom: Optional[str] = Field(None, description='Inherited from')
        inheritedRole: Optional[str] = Field(None, description='Inherited role')
        hasDirectAccess: Optional[bool] = Field(None, description='Has direct access')
        role: Optional[str] = Field(None, description='Role')
        email: Optional[str] = Field(None, description='Email')
        lastName: Optional[str] = Field(None, description='Last name')
        firstName: Optional[str] = Field(None, description='First name')
        userUuid: Optional[str] = Field(None, description='UUID of the user')

    slug: str = Field(..., description='The slug of the space')
    pinnedListOrder: Optional[float] = Field(
        None, description='The order of the pinned list'
    )
    pinnedListUuid: Optional[str] = Field(
        None, description='The UUID of the pinned list'
    )
    groupsAccess: Optional[List[GroupAccess]] = Field(
        None, description='Groups access details'
    )
    access: Optional[List[Access]] = Field(None, description='Access details')
    projectUuid: str = Field(..., description='The UUID of the project')
    isPrivate: bool = Field(..., description='Whether the space is private')
    name: str = Field(..., description='The name of the space')
    uuid: str = Field(..., description='The UUID of the space')
    organizationUuid: str = Field(..., description='The UUID of the organization')

    @classmethod
    @override
    def from_response(
        cls, response: requests.Response
    ) -> 'CreateSpaceInProjectApiV1Response':
        space_data = response.json().get('results', {})
        return cls(**space_data)


class CreateSpaceInProject(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.POST
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}/spaces'

    def request(self, projectUuid: str) -> CreateSpaceInProjectApiV1Response:
        response = self.client.call(
            request_type=RequestType.POST,
            path=self.__class__.path.format(projectUuid=projectUuid),
            data=self.request_body.model_dump(),
        )
        return CreateSpaceInProjectApiV1Response.from_response(response=response)
