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

from typing import ClassVar, Optional

from pydantic import Field

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               BaseResponseModel, RequestType)
from lightdash_ops.models.organization import OrganizationRole


# pylint: disable=invalid-name
class GetOrganizationMemberByUuidApiV1Response(BaseResponseModel):
    isInviteExpired: Optional[bool] = Field(
        default=None,
        description="Whether the user's invite to the organization has expired",
    )
    isActive: bool = Field(
        ...,
        description='Whether the user has accepted their invite to the organization',
    )
    role: OrganizationRole = Field(
        ...,
        description='The role of the member',
    )
    organizationUuid: str = Field(
        ...,
        description='Unique identifier for the organization the user is a member of',
    )
    email: str = Field(..., description='The email of the member')
    lastName: str = Field(..., description='The last name of the member')
    firstName: str = Field(..., description='The first name of the member')
    userUuid: str = Field(..., description='Unique identifier for the user')


class GetOrganizationMemberByUuid(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/org/users/{userUuid}'

    def request(self, user_uuid: str) -> GetOrganizationMemberByUuidApiV1Response:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path.format(userUuid=user_uuid),
        )
        return GetOrganizationMemberByUuidApiV1Response.from_response(response=response)
