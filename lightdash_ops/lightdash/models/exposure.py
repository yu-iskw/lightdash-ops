#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List, Optional

from pydantic import BaseModel, Field

from lightdash_ops.lightdash.v1.get_dbt_exposures import DbtExposure


class DbtExposureProperty(BaseModel):
    class Config:
        extra = 'allow'

    name: str = Field(..., description='The name of the exposure')
    description: Optional[str] = Field(None, description='A brief description of the exposure')
    type: str = Field(..., description='The type of the exposure')
    url: str = Field(..., description='The URL associated with the exposure')
    maturity: Optional[str] = Field(None, description='The maturity level of the exposure')
    tags: Optional[List[str]] = Field(None, description='A list of tags associated with the exposure')
    meta: Optional[dict] = Field(None, description='Metadata related to the exposure')
    owner: dict = Field(..., description='The owner information of the exposure')
    depends_on: List[str] = Field(..., description='A list of dependencies for the exposure')
    label: str = Field(..., description='The label of the exposure')

    @classmethod
    def from_dbt_exposure(cls, exposure: DbtExposure):
        return cls(
            name=exposure.name.replace('-', '_'),
            description=exposure.description,
            type=exposure.type,
            url=exposure.url,
            maturity=exposure.maturity,
            tags=exposure.tags,
            meta=exposure.meta,
            owner=exposure.owner.model_dump(),
            depends_on=exposure.depends_on,
            label=exposure.label,
        )
