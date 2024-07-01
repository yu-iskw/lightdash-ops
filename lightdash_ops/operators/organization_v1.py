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

from typing import List, Optional

import loguru
from pydantic import BaseModel, EmailStr, Field

from lightdash_ops.lightdash.v1.client import LightdashClient
from lightdash_ops.lightdash.v1.get_organization_member_by_uuid import \
    GetOrganizationMemberByUuid
from lightdash_ops.lightdash.v1.list_organization_members import \
    ListOrganizationMembers
from lightdash_ops.lightdash.v1.list_organization_projects import \
    ListOrganizationProjects
from lightdash_ops.models.organization import (OrganizationMember,
                                               OrganizationRole)
from lightdash_ops.models.project import Project, ProjectType

logger = loguru.logger


class CachedOrganizationMembers:
    """Cached organization members"""

    # pylint: disable=invalid-name
    __members: Optional[List[OrganizationMember]] = None

    @classmethod
    def get_members(cls, client: LightdashClient) -> List[OrganizationMember]:
        """Get all members of an organization"""
        if cls.__members is None:
            # Get all members in the organization if they are not cached
            operator = OrganizationOperatorV1(client=client)
            cls.__members = operator.get_organization_members()
        return cls.__members


class OrganizationOperatorV1(BaseModel):
    """
    An operator class to deal with Lightdash projects
    """

    client: LightdashClient = Field(..., description='Lightdash client')

    class Config:
        arbitrary_types_allowed = True

    def get_projects(self) -> List[Project]:
        """Get all projects in an organization"""
        formatted_projects = []
        list_organization_projects = ListOrganizationProjects(client=self.client)
        response = list_organization_projects.request()
        for project in response.projects:
            formatted_projects.append(
                Project(
                    type=ProjectType(str(project.type)),
                    name=project.name,
                    uuid=project.projectUuid,
                )
            )
        return formatted_projects

    # To avoid the frequent API calls, we cache the results
    def get_organization_members(self) -> List[OrganizationMember]:
        """Get all members in an organization"""
        # Get all members
        list_organization_members = ListOrganizationMembers(client=self.client)
        response = list_organization_members.request()
        # Format
        formatted_members = []
        for member in response.members:
            formatted_members.append(
                OrganizationMember(
                    email=member.email,
                    uuid=member.userUuid,
                    role=OrganizationRole(member.role),
                    is_active=member.isActive,
                )
            )
        return formatted_members

    def get_organization_member_by_email(
        self, email: str
    ) -> Optional[OrganizationMember]:
        """Get a member in an organization by email"""
        organization_members = CachedOrganizationMembers.get_members(client=self.client)
        # pylint: disable=not-an-iterable
        for member in organization_members:
            if member.email == email:
                return member
        return None

    def get_organization_member_by_uuid(
        self, user_uuid: str
    ) -> Optional[OrganizationMember]:
        """Get a member in an organization by user UUID"""
        get_member_by_uuid = GetOrganizationMemberByUuid(client=self.client)
        response = get_member_by_uuid.request(user_uuid=user_uuid)
        return OrganizationMember(
            email=EmailStr(response.email),
            uuid=response.userUuid,
            role=response.role,
            is_active=response.isActive,
        )
