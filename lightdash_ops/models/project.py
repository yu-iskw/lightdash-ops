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

from lightdash_ops.models.project_member import ProjectMember, ProjectRole
from lightdash_ops.models.space import Space


class ProjectType(str, enum.Enum):
    """Project type"""
    DEFAULT = 'DEFAULT'
    PREVIEW = 'PREVIEW'


class Project(BaseModel):
    """Information about a Lightdash project"""
    type: ProjectType = Field(description='Project type', default=None)
    name: str = Field(description='Project name')
    uuid: str = Field(description='Project UUID')
    description: str = Field(description='Project description', default=None)
    members: List[ProjectMember] = Field(description='Project members',
                                         default_factory=list)
    spaces: List[Space] = Field(description='Spaces. The names of spaces must be unique.',
                                default_factory=list)

    # pylint: disable=no-self-argument,no-self-use
    @validator('members')
    def check_at_least_one_admin(cls, v):
        """Check if there is at least one admin"""
        if not any(member.role == ProjectRole.ADMIN for member in v):
            raise ValueError('There must be at least one admin')
        return v

    # pylint: disable=no-self-argument,no-self-use
    @validator('spaces')
    def check_duplicated_spaces(cls, value):
        """Check if names of the spaces are duplicated"""
        names = [space.name for space in value]
        if len(names) != len(set(names)):
            raise ValueError('Space names must be unique')
        return value

    def get_space_by_name(self, space_name: str) -> Optional[Space]:
        """Get space by name"""
        for space in self.spaces:
            if space.name == space_name:
                return space
        return None
