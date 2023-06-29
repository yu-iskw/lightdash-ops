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

import datetime
from typing import List

from pydantic import BaseModel, Field, ValidationError, validator

from lightdash_ops.models.base_user import LightdashUser


class GroupMember(LightdashUser):
    """Information about a Lightdash user group member"""
    pass


class UserGroup(BaseModel):
    enabled: bool = Field(description='User group enabled', default=True)
    uuid: str = Field(description='User group UUID', default=None)
    name: str = Field(description='User group name')
    members: List[GroupMember] = Field(description='List of members in the group', default_factory=list)
    organization_uuid: str = Field(description='Organization UUID', default=None)
    created_at: datetime.datetime = Field(description='User group created at', default=None)

    # pylint: disable=no-self-argument,no-self-use
    @validator('members')
    def check_duplicated_members(cls, v):
        """Check if there are duplicated members"""
        if len(v) != len(set(v)):
            raise ValidationError('There are duplicated members')
        return v
