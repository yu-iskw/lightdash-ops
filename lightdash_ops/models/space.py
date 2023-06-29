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
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from lightdash_ops.models.user_group import LightdashUser


class SpaceMember(LightdashUser):
    """Information about a Lightdash space member"""
    pass


class SpaceVisibility(enum.Enum):
    """Space visibility"""
    PUBLIC = 'public'
    PRIVATE = 'private'

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_private(cls, visibility: 'SpaceVisibility') -> bool:
        """Check if visibility is private"""
        if visibility == SpaceVisibility.PRIVATE:
            return True
        return False

    @classmethod
    def get_visibility(cls, is_private: bool) -> 'SpaceVisibility':
        """Get visibility by is_private"""
        if is_private is True:
            return SpaceVisibility.PRIVATE
        return SpaceVisibility.PUBLIC


class Space(BaseModel):
    """Information about a Lightdash space"""
    name: str = Field(description='Space name')
    project_uuid: str = Field(description='Project UUID', default=None)
    uuid: str = Field(description='Space UUID', default=None)
    visibility: SpaceVisibility = Field(description='Space visibility')
    description: str = Field(description='Space description')
    allow_manual_management: bool = Field(description='Allow manual management', default=False)
    members: List[SpaceMember] = Field(description='Space members', default_factory=list)

    # pylint: disable=no-self-argument,no-self-use
    @validator('allow_manual_management', always=True)
    def validate_allow_manual_management_and_visibility(cls, value, values):
        """Check if visibility is public and allow_manual_management is False"""
        allow_manual_management = value
        visibility = values.get('visibility')
        if visibility == SpaceVisibility.PRIVATE and allow_manual_management is True:
            raise ValueError('allow_manual_management must be False if visibility is public')
        return value

    def get_member_by_email(self, email: str) -> Optional[SpaceMember]:
        """Get a member by email"""
        for m in self.members:
            if m.email == email:
                return m
        return None

    def __eq__(self, other) -> bool:
        """Compare with another Space"""
        if not isinstance(other, Space):
            raise ValueError("Can't compare with a non Space")
        if self.name == other.name or self.uuid == other.uuid:
            return True
        return False
