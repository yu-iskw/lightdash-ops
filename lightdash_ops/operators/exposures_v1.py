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

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from lightdash_ops.lightdash.v1.client import LightdashClient
from lightdash_ops.lightdash.v1.get_dbt_exposures import GetDbtExposures
from lightdash_ops.lightdash.v1.list_organization_projects import \
    ListOrganizationProjects
from lightdash_ops.models.exposure import DbtExposureProperty


class DbtExposuresProperties(BaseModel):
    version: Optional[int] = Field(default=2, description='Version of the exposures')
    exposures: List[DbtExposureProperty] = Field(..., description='List of exposures')


class DbtExposuresOperatorV1(BaseModel):
    client: LightdashClient = Field(..., description='Lightdash client')

    def get_dbt_exposures_in_all_projects(
        self,
        exposure_types: Optional[List[str]] = None,
        project_names: Optional[List[str]] = None,
    ) -> Dict[str, DbtExposuresProperties]:
        """Get dbt exposures for all projects."""
        exposures = {}
        # Get all projects
        list_organization_projects = ListOrganizationProjects(client=self.client)
        list_organization_projects_response = list_organization_projects.request()
        for project in list_organization_projects_response.projects:
            # Skip non-default projects not to collect preview projects
            if project.type.upper() != 'DEFAULT':
                continue
            # Filter projects by name
            if project_names is not None and len(project_names) > 0 and project.name not in project_names:
                continue
            exposures[project.name] = self.get_dbt_exposures_in_project(
                project_uuid=project.projectUuid, exposure_types=exposure_types
            )
        return exposures

    def get_dbt_exposures_in_project(
        self, project_uuid: str, exposure_types: Optional[List[str]] = None
    ) -> DbtExposuresProperties:
        """Get dbt exposures for a project."""
        get_dbt_exposures = GetDbtExposures(client=self.client)
        response = get_dbt_exposures.request(project_uuid=project_uuid)
        exposures = []
        for _, exposure in response.results.items():
            if len(exposure.depends_on) == 0:
                continue
            elif exposure_types is not None and exposure.type not in exposure_types:
                continue
            exposures.append(DbtExposureProperty.from_dbt_exposure(exposure=exposure))
        return DbtExposuresProperties(exposures=exposures)
