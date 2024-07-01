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
class ListSpacesInProjectApiV1Response(BaseResponseModel):

    class Space(BaseModel):
        class UserAccess(BaseModel):
            class Config:
                extra = 'allow'
            inheritedFrom: Optional[str] = Field(None, description='Inherited from entity')
            inheritedRole: Optional[str] = Field(None, description='Inherited role')
            hasDirectAccess: bool = Field(..., description='Whether the user has direct access')
            role: str = Field(..., description='Role of the user in the space')
            email: str = Field(..., description='Email of the user')
            lastName: str = Field(..., description='Last name of the user')
            firstName: str = Field(..., description='First name of the user')
            userUuid: str = Field(..., description='Unique identifier of the user')
        class Config:
            extra = 'allow'
        name: str = Field(..., description='The name of the space')
        uuid: str = Field(..., description='The unique identifier of the space')
        projectUuid: str = Field(..., description='The unique identifier of the project')
        organizationUuid: str = Field(..., description='The unique identifier of the organization')
        # pinnedListUuid: str = Field(..., description="The unique identifier of the pinned list")
        isPrivate: bool = Field(..., description='Whether the space is private')
        # pinnedListOrder: float = Field(..., description="The order of the pinned list")
        slug: str = Field(..., description='The slug of the space')
        access: List[str] = Field(..., description='List of access permissions')
        userAccess: Optional[UserAccess] = Field(default_factory=UserAccess, description='User access details')

    spaces: List[Space] = Field(
        ..., default_factory=list, description='List of spaces'
    )

    @classmethod
    def from_response(
        cls, response: requests.Response
    ) -> 'ListSpacesInProjectApiV1Response':
        results = response.json().get('results', [])
        return cls.from_results(results)

    @classmethod
    def from_results(cls, results: list) -> 'ListSpacesInProjectApiV1Response':
        spaces = []
        for space in results:
            try:
                spaces.append(cls.Space(**space))
            except Exception as e:
                raise ValueError(f'Failed to parse spaces: {space}') from e
        # spaces = [cls.Space(**space) for space in results]
        return cls(spaces=spaces)


class ListSpacesInProject(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}/spaces'

    def request(self, project_uuid: str) -> ListSpacesInProjectApiV1Response:
        response = self.client.call(
            request_type=self.__class__.request_type,
            path=self.__class__.path.format(projectUuid=project_uuid),
        )
        return ListSpacesInProjectApiV1Response.from_response(response=response)
