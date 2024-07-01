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


# pylint: disable=invalid-name
class GetAuthenticatedUserApiV1Response(BaseResponseModel):
    userUuid: str = Field(..., description='The unique identifier of the user')
    email: str = Field(..., description='The email of the user')
    firstName: str = Field(..., description='The first name of the user')
    lastName: str = Field(..., description='The last name of the user')
    organizationUuid: Optional[str] = Field(
        default=None, description='The unique identifier of the organization'
    )
    organizationName: Optional[str] = Field(
        default=None, description='The name of the organization'
    )
    organizationCreatedAt: Optional[str] = Field(
        default=None,
        description='The creation date of the organization',
        format='date-time',
    )
    isTrackingAnonymized: bool = Field(
        ..., description='Whether tracking is anonymized'
    )
    isMarketingOptedIn: bool = Field(
        ..., description='Whether the user is opted in to marketing'
    )
    isSetupComplete: bool = Field(..., description='Whether the setup is complete')
    role: Optional[str] = Field(
        default=None,
        description='The role of the user in the organization',
        enum=['member', 'viewer', 'interactive_viewer', 'editor', 'developer', 'admin'],
    )
    isActive: bool = Field(..., description='Whether the user is active')
    additionalProperties: dict = Field(
        default_factory=dict, description='Additional properties'
    )


class GetAuthenticatedUser(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/user'

    def request(self) -> GetAuthenticatedUserApiV1Response:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path,
        )
        return GetAuthenticatedUserApiV1Response.from_response(response=response)
