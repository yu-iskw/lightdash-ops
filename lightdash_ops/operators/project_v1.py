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

from typing import Dict, List, Optional

import loguru
from lightdash_client import AuthenticatedClient
from lightdash_client.models import GrantProjectAccessToUserResponse200
from lightdash_client.types import Response
from pydantic import BaseModel, EmailStr, Field

from lightdash_ops.lightdash.project import (get_project_members,
                                             grant_project_member_role,
                                             revoke_project_access)
from lightdash_ops.lightdash.space import get_spaces as get_lightdash_spaces
from lightdash_ops.lightdash.space import grant_space_role
from lightdash_ops.lightdash.space import \
    revoke_space_role as revoke_lightdash_space_role
from lightdash_ops.models.project_member import ProjectRole
from lightdash_ops.models.space import Space, SpaceMember, SpaceVisibility
from lightdash_ops.operators.organization_v1 import OrganizationOperatorV1
from lightdash_ops.utils import mask_text

logger = loguru.logger


class ProjectOperatorV1(BaseModel):
    """
    An operator class to deal with Lightdash projects
    """
    client: AuthenticatedClient = Field(..., description='Lightdash client')

    class Config:
        arbitrary_types_allowed = True

    def grant_project_member_role_by_email(
            self,
            project_uuid: str,
            email: str,
            role: ProjectRole,
            dry_run: bool = True) -> Optional[Response[GrantProjectAccessToUserResponse200]]:
        """Grant a project role to a member"""
        logger.info(f'Would grant the project role {role} to {mask_text(email)} in the project {project_uuid}')
        if dry_run is False:
            response = grant_project_member_role(
                client=self.client, project_uuid=project_uuid, email=email, role=role)
            return response
        return None

    def revoke_project_member_role_by_uuid(
            self,
            project_uuid: str,
            user_uuid: str,
            dry_run: bool = True
    ):
        """Revoke a project role from a member by user UUID"""
        logger.info(f'Would revoke the project role from {user_uuid} in the project {project_uuid}')
        if dry_run is False:
            response = revoke_project_access(
                client=self.client, project_uuid=project_uuid, user_uuid=user_uuid)
            return response
        return None

    def revoke_project_member_role_by_email(
            self,
            project_uuid: str,
            email: str,
            dry_run: bool = True
    ):
        """Revoke a project role from a member by email"""
        organization_operator = OrganizationOperatorV1(client=self.client)
        member = organization_operator.get_organization_member_by_email(email=email)
        if member is None:
            raise ValueError(f'User {email} does not exist in the organization')
        return self.revoke_project_member_role_by_uuid(
            project_uuid=project_uuid, user_uuid=member.uuid, dry_run=dry_run)

    def get_spaces(self, project_uuid: str) -> List[Space]:
        """Get all spaces in a project"""
        # Get the current members of the project
        organization_operator = OrganizationOperatorV1(client=self.client)
        organization_members = {m.uuid: m
                                for m in organization_operator.get_organization_members()}
        # Get spaces
        spaces = get_lightdash_spaces(client=self.client, project_uuid=project_uuid)
        # Format spaces
        formatted_spaces = []
        for s in spaces:
            space_member_emails = [
                SpaceMember(email=EmailStr(organization_members[user_uuid].email))
                for user_uuid in s.access
                if user_uuid in organization_members
            ]
            formatted_spaces.append(
                Space(name=s.name,
                      uuid=s.uuid,
                      visibility=SpaceVisibility.get_visibility(s.is_private),
                      members=space_member_emails,
                      description='')
            )
        return formatted_spaces

    def get_space_by_name(
            self,
            project_uuid: str,
            space_name: str) -> Optional[Space]:
        """Get a space by name"""
        # Get organization members
        organization_operator = OrganizationOperatorV1(client=self.client)
        organization_members = {
            m.uuid: m
            for m in organization_operator.get_organization_members()
        }
        # Get spaces
        spaces = get_lightdash_spaces(client=self.client, project_uuid=project_uuid)
        # Find the space
        for s in spaces:
            if space_name == s.name:
                space_members = [
                    SpaceMember(
                        uuid=user_uuid,
                        email=EmailStr(organization_members[user_uuid].email)
                    )
                    for user_uuid in s.access
                ]
                return Space(
                    name=s.name,
                    uuid=s.uuid,
                    visibility=SpaceVisibility.get_visibility(s.is_private),
                    members=space_members,
                    description='')
        return None

    def get_project_members(self, project_uuid: str) -> List[Dict[str, str]]:
        """Get the members of a project"""
        formatted_members = []
        # Get all members of a project
        members = get_project_members(client=self.client, project_uuid=project_uuid)
        # Format
        for member in members:
            formatted_members.append({
                'email': member.email,
                'uuid': member.user_uuid,
                'role': member.role,
            })
        return formatted_members

    def grant_space_role(
            self, project_uuid: str, space_uuid: str, user_uuid: str, dry_run: bool = True):
        """Add a user to a space"""
        logger.info(f'Will grant access to space {space_uuid} to user {user_uuid}')
        if dry_run is False:
            response = grant_space_role(
                client=self.client,
                project_uuid=project_uuid,
                space_uuid=space_uuid,
                user_uuid=user_uuid,
            )
            logger.info(f'Granted access to space {space_uuid} to user {user_uuid}')
            return response
        return None

    def revoke_space_role(
            self, project_uuid: str, space_uuid: str, user_uuid: str, dry_run: bool = True):
        """Revokes a user from a space"""
        logger.info(f'Will grant access to space {space_uuid} to user {user_uuid}')
        if dry_run is False:
            response = revoke_lightdash_space_role(
                client=self.client, project_uuid=project_uuid, space_uuid=space_uuid, user_uuid=user_uuid)
            logger.info(f'Revoked access to space {space_uuid} from user {user_uuid}')
            return response
        return None
