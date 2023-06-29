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

import enum
from typing import List

from lightdash_client.models import OrganizationMemberRole
from pydantic import BaseModel, EmailStr, Field, ValidationError, validator


class OrganizationRole(str, enum.Enum):
    """Organization role"""
    ADMIN = 'admin'
    DEVELOPER = 'developer'
    EDITOR = 'editor'
    INTERACTIVE_VIEWER = 'interactive_viewer'
    MEMBER = 'member'
    VIEWER = 'viewer'

    def __str__(self) -> str:
        return self.value

    def to_lightdash_expression(self) -> OrganizationMemberRole:
        """Convert to lightdash role"""
        return OrganizationMemberRole(self.value)


class OrganizationMember(BaseModel):
    uuid: str = Field(description='Member UUID', default=None)
    email: EmailStr = Field(description='Member email')
    role: OrganizationRole = Field(description='Member role')
    is_active: bool = Field(description='Member is active', default=True)


class Organization(BaseModel):
    """Information about a Lightdash organization"""
    uuid: str = Field(description='Organization UUID', default=None)
    members: List[OrganizationMember] = Field(description='Organization members', default_factory=list)

    # pylint: disable=no-self-argument,no-self-use
    @validator('members')
    def check_at_least_one_admin(cls, v):
        """Check if there is at least one admin"""
        if not any(member.role == OrganizationRole.ADMIN for member in v):
            raise ValidationError('There must be at least one admin')
        return v


class OrganizationConfigV1(BaseModel):
    """Organization config v1"""
    allow_manual_management: bool = Field(description='Allow manual management', default=False)
    organization: Organization = Field(description='Organization')
