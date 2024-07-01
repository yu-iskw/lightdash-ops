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
class GetExploreApiV1Response(BaseResponseModel):
    sqlPath: Optional[str] = Field(
        default=None,
        description='The SQL path of the explore',
    )
    ymlPath: Optional[str] = Field(
        default=None,
        description='The YML path of the explore',
    )
    warehouse: Optional[str] = Field(
        default=None,
        description='The warehouse of the explore',
    )
    targetDatabase: Optional[str] = Field(
        default=None,
        description='The target database of the explore',
    )
    tables: Optional[dict] = Field(
        default=None,
        description='The tables in the explore',
    )
    joinedTables: Optional[list] = Field(
        default=None,
        description='The joined tables in the explore',
    )
    baseTable: Optional[str] = Field(
        default=None,
        description='The base table of the explore',
    )
    groupLabel: Optional[str] = Field(
        default=None,
        description='The group label of the explore',
    )
    tags: Optional[list] = Field(
        default=None,
        description='The tags of the explore',
    )
    label: Optional[str] = Field(
        default=None,
        description='The label of the explore',
    )
    name: Optional[str] = Field(
        default=None,
        description='The name of the explore',
    )
    status: Optional[str] = Field(
        default=None,
        description='The status of the explore',
    )


class GetExplore(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}/explores/{exploreId}'

    def request(self, projectUuid: str, exploreId: str) -> GetExploreApiV1Response:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path.format(projectUuid=projectUuid, exploreId=exploreId),
        )
        return GetExploreApiV1Response.from_response(response=response)
