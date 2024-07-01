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
#

from typing import List

import loguru
from pydantic import BaseModel, Field

from lightdash_ops.lightdash.v1.client import LightdashClient
from lightdash_ops.lightdash.v1.list_project_members import ListProjectMembers
from lightdash_ops.lightdash.v1.list_spaces_in_project import \
    ListSpacesInProject
from lightdash_ops.models.organization import OrganizationMember
from lightdash_ops.models.project import Project

logger = loguru.logger

class ProjectOperatorV1(BaseModel):
    """
    An operator class to deal with Lightdash projects
    """

    client: LightdashClient = Field(..., description='Lightdash client')

    class Config:
        arbitrary_types_allowed = True

    def get_spaces(self, project_uuid: str) -> List[Project]:
        """Get all spaces in a project"""
        list_project_spaces = ListSpacesInProject(client=self.client)
        response = list_project_spaces.request(project_uuid=project_uuid)
        return response.spaces

    def get_project_members(self, project_uuid: str) -> List[OrganizationMember]:
        """Get all members in a project"""
        list_project_members = ListProjectMembers(client=self.client)
        response = list_project_members.request(project_uuid=project_uuid)
        return response.members
