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
class GetProjectApiV1Response(BaseResponseModel):
    dbtVersion: Optional[str] = Field(
        default=None,
        description='The version of dbt used in the project',
    )
    upstreamProjectUuid: Optional[str] = Field(
        default=None,
        description='The UUID of the upstream project',
    )
    pinnedListUuid: Optional[str] = Field(
        default=None,
        description='The UUID of the pinned list',
    )
    warehouseConnection: Optional[dict] = Field(
        default=None,
        description='The warehouse connection details',
    )
    dbtConnection: Optional[dict] = Field(
        default=None,
        description='The dbt connection details',
    )
    type: str = Field(..., description='The type of the project')
    name: str = Field(..., description='The name of the project')
    projectUuid: str = Field(..., description='The unique identifier of the project')
    organizationUuid: str = Field(
        ..., description='The unique identifier of the organization'
    )


class GetProject(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}'

    def request(self, projectUuid: str) -> GetProjectApiV1Response:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path.format(projectUuid=projectUuid),
        )
        return GetProjectApiV1Response.from_response(response=response)
