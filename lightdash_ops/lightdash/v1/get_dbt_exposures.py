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

from typing import Any, ClassVar, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from lightdash_ops.lightdash.v1.client import (BaseLightdashApiCaller,
                                               RequestType)


class DbtExposure(BaseModel):
    class Config:
        extra = 'allow'

    class DbtExposureOwner(BaseModel):
        class Config:
            extra = 'allow'

        name: str = Field(..., description='Name of the exposure owner')
        email: Optional[str] = Field(None, description='Email of the exposure owner')

    name: str = Field(..., description='Name of the exposure')
    description: Optional[str] = Field(None, description='Description of the exposure')
    type: str = Field(..., description='Type of the exposure')
    owner: DbtExposureOwner = Field(..., description='Owner of the exposure')
    depends_on: List[str] = Field(..., alias='dependsOn', description='List of dependencies for the exposure')
    url: Optional[str] = Field(None, description='URL of the exposure')
    maturity: Optional[str] = Field(None, description='Maturity level of the exposure')
    tags: Optional[List[str]] = Field(None, description='Tags associated with the exposure')
    meta: Optional[Dict[str, Any]] = Field(None, description='Metadata for the exposure')
    config: Optional[Dict[str, Any]] = Field(None, description='Configuration for the exposure')
    created_at: Optional[str] = Field(None, description='Creation timestamp of the exposure')
    updated_at: Optional[str] = Field(None, description='Last update timestamp of the exposure')
    label: Optional[str] = Field(None, description='Label of the exposure')  # Added field to match file_context_0


class GetDbtExposuresResponse(BaseModel):
    status: str
    results: Dict[str, DbtExposure]

    @classmethod
    def from_response(cls, response: requests.Response) -> 'GetDbtExposuresResponse':
        response_data = response.json()
        status = response_data.get('status')
        results_data = response_data.get('results', {})
        return cls(status=status, results=cls.from_dict(results_data))

    @classmethod
    def from_dict(cls, data: dict) -> Dict[str, DbtExposure]:
        results = {}
        for key, value in data.items():
            try:
                results.update({key: DbtExposure(**value)})
            except Exception as e:
                raise ValueError(f"Can't parse {value}") from e
        return results



class GetDbtExposures(BaseLightdashApiCaller):
    request_type: ClassVar[RequestType] = RequestType.GET
    path: ClassVar[str] = '/api/v1/projects/{projectUuid}/dbt-exposures'

    def request(self, project_uuid: str) -> GetDbtExposuresResponse:
        response = self.client.call(
            request_type=RequestType.GET,
            path=self.__class__.path.format(projectUuid=project_uuid),
        )
        return GetDbtExposuresResponse.from_response(response)
