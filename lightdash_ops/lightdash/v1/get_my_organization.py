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

from pydantic import Field

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               BaseResponseModel, RequestType)


# pylint: disable=invalid-name
class GetOrganizationApiV1Response(BaseResponseModel):
    defaultProjectUuid: Optional[str] = Field(
        default=None,
        description='The project a user sees when they first log in to the organization',
    )
    needsProject: Optional[bool] = Field(
        default=None,
        description="The organization needs a project if it doesn't have at least one project.",
    )
    chartColors: Optional[List[str]] = Field(
        default=None,
        description='The default color palette for all projects in the organization',
    )
    name: str = Field(..., description='The name of the organization')
    organizationUuid: str = Field(
        ..., description='The unique identifier of the organization'
    )


class GetOrganization(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/org'

    def request(self) -> GetOrganizationApiV1Response:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path,
        )
        return GetOrganizationApiV1Response.from_response(response=response)
