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
from lightdash_client import AuthenticatedClient
from pydantic import BaseModel, EmailStr, Field

from lightdash_ops.lightdash.organization import (
    get_organization_members, get_projects, update_organization_member_role)
from lightdash_ops.models.organization import (OrganizationMember,
                                               OrganizationRole)
from lightdash_ops.models.project import Project, ProjectType

logger = loguru.logger


class CachedOrganizationMembers:
    """Cached organization members"""
    # pylint: disable=invalid-name
    __members: List[OrganizationMember] = None  # type: ignore[assignment]

    @classmethod
    def get_members(
            cls, client: AuthenticatedClient) -> List[OrganizationMember]:
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
    client: AuthenticatedClient = Field(..., description='Lightdash client')

    class Config:
        arbitrary_types_allowed = True

    def get_projects(self) -> List[Project]:
        """Get all projects in an organization"""
        formatted_projects = []
        projects = get_projects(client=self.client)
        for project in projects:
            formatted_projects.append(
                Project(
                    type=ProjectType(str(project.type)),
                    name=project.name,
                    uuid=project.project_uuid,
                )
            )
        return formatted_projects

    # To avoid the frequent API calls, we cache the results
    def get_organization_members(self) -> List[OrganizationMember]:
        """Get all members in an organization"""
        # Get all members
        members = get_organization_members(client=self.client)
        # Format
        formatted_members = []
        for member in members:
            formatted_members.append(OrganizationMember(
                email=EmailStr(member.email),
                uuid=member.user_uuid,
                role=OrganizationRole(member.role),
                is_active=member.is_active,
            ))
        return formatted_members

    def get_organization_member_by_email(self, email: str) -> Optional[OrganizationMember]:
        """Get a member in an organization by email"""
        organization_members = CachedOrganizationMembers.get_members(client=self.client)
        # pylint: disable=not-an-iterable
        for member in organization_members:
            if member.email == email:
                return member
        return None

    def get_organization_member_by_uuid(self, user_uuid: str) -> Optional[OrganizationMember]:
        """Get a member in an organization by user UUID"""
        organization_members = CachedOrganizationMembers.get_members(client=self.client)
        # pylint: disable=not-an-iterable
        for member in organization_members:
            if member.uuid == user_uuid:
                return member
        return None

    def update_member_role(self, user_uuid: str, role: OrganizationRole, dry_run: bool = False):
        """Update a member's role"""
        logger.info(f'Will update member {user_uuid} to role {role}')
        if dry_run is False:
            response = update_organization_member_role(
                client=self.client, user_uuid=user_uuid, role=role)
            return response
        return None

    def update_member_role_by_email(self, email: str, role: OrganizationRole, dry_run: bool = False):
        """Update a member's role by email"""
        member = self.get_organization_member_by_email(email=email)
        if member is None:
            raise ValueError(f'No member with email {email}')
        return self.update_member_role(user_uuid=member.uuid, role=role, dry_run=dry_run)
