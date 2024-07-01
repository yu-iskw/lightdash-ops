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
from pydantic import Field

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               BaseResponseModel, RequestType)


# pylint: disable=invalid-name
class GetSpaceApiV1Response(BaseResponseModel):
    class SpaceGroup(BaseResponseModel):
        spaceRole: str = Field(..., description='The role of the group in the space')
        groupName: str = Field(..., description='The name of the group')
        groupUuid: str = Field(..., description='The UUID of the group')

    class SpaceShare(BaseResponseModel):
        inheritedFrom: str = Field(..., description='The source of the inherited access')
        inheritedRole: str = Field(..., description='The role inherited from the source')
        hasDirectAccess: bool = Field(..., description='Whether the user has direct access')
        role: str = Field(..., description='The role of the user in the space')
        email: str = Field(..., description='The email of the user')
        lastName: str = Field(..., description='The last name of the user')
        firstName: str = Field(..., description='The first name of the user')
        userUuid: str = Field(..., description='The UUID of the user')

    class SpaceDashboard(BaseResponseModel):
        name: str = Field(..., description='The name of the dashboard')
        description: Optional[str] = Field(None, description='The description of the dashboard')
        uuid: str = Field(..., description='The UUID of the dashboard')
        spaceUuid: str = Field(..., description='The UUID of the space')
        projectUuid: str = Field(..., description='The UUID of the project')
        organizationUuid: str = Field(..., description='The UUID of the organization')
        pinnedListUuid: Optional[str] = Field(None, description='The UUID of the pinned list')
        updatedAt: str = Field(..., description='The last update timestamp of the dashboard')
        updatedByUser: Optional[dict] = Field(None, description='The user who last updated the dashboard')
        views: float = Field(..., description='The number of views of the dashboard')
        firstViewedAt: Optional[str] = Field(None, description='The first view timestamp of the dashboard')
        pinnedListOrder: Optional[float] = Field(None, description='The order of the pinned list')
        validationErrors: Optional[List[dict]] = Field(None, description='The validation errors of the dashboard')
        slug: str = Field(..., description='The slug of the space')

    name: str = Field(..., description='The name of the space')
    uuid: str = Field(..., description='The UUID of the space')
    organizationUuid: str = Field(..., description='The UUID of the organization')
    projectUuid: str = Field(..., description='The UUID of the project')
    isPrivate: bool = Field(..., description='Whether the space is private')
    status: str = Field(..., description='The status of the space')
    groupsAccess: List[SpaceGroup] = Field(..., description='The groups with access to the space')
    access: List[SpaceShare] = Field(..., description='The users with access to the space')
    dashboards: List[SpaceDashboard] = Field(..., description='The dashboards in the space')
    queries: List[dict] = Field(..., description='The queries in the space')

    @staticmethod
    def from_response(response: requests.Response) -> 'GetSpaceApiV1Response':
        results = response.json().get('results', {})
        return GetSpaceApiV1Response.model_validate(results)

    @staticmethod
    def from_dict(data: dict) -> 'GetSpaceApiV1Response':
        return GetSpaceApiV1Response.model_validate(data)


class GetSpace(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}/spaces/{spaceUuid}'

    def request(self, projectUuid: str, spaceUuid: str) -> GetSpaceApiV1Response:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path.format(projectUuid=projectUuid, spaceUuid=spaceUuid),
        )
        return GetSpaceApiV1Response.from_response(response=response)
