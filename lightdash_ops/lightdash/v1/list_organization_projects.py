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
class ListOrganizationProjectsApiV1Response(BaseResponseModel):
    class Project(BaseModel):
        requireUserCredentials: bool = Field(
            ..., description='Whether user credentials are required'
        )
        warehouseType: str = Field(..., description='The type of warehouse')
        type: str = Field(..., description='The type of project')
        name: str = Field(..., description='The name of the project')
        projectUuid: str = Field(
            ..., description='The unique identifier of the project'
        )

    projects: List[Project] = Field(
        ..., default_factory=list, description='List of projects'
    )

    @classmethod
    def from_response(
        cls, response: requests.Response
    ) -> 'ListOrganizationProjectsApiV1Response':
        results = response.json().get('results', [])
        return cls.from_results(results)

    @classmethod
    def from_results(cls, results: dict) -> 'ListOrganizationProjectsApiV1Response':
        projects = [cls.Project(**project) for project in results]
        return cls(projects=projects)


class ListOrganizationProjects(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/org/projects'

    def request(self) -> ListOrganizationProjectsApiV1Response:
        response = self.client.call(
            request_type=self.__class__.request_type,
            path=self.__class__.path,
        )
        return ListOrganizationProjectsApiV1Response.from_response(response=response)
