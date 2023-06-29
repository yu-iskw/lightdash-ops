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
import enum

from lightdash_client.models import ProjectMemberRole
from pydantic import Field, FutureDate, ValidationError, validator

from lightdash_ops.models.base_user import LightdashUser
from lightdash_ops.models.settings import get_settings
from lightdash_ops.utils import is_future_date


class ProjectRole(str, enum.Enum):
    """Project roles"""
    ADMIN = 'admin'
    DEVELOPER = 'developer'
    EDITOR = 'editor'
    INTERACTIVE_VIEWER = 'interactive_viewer'
    VIEWER = 'viewer'
    MEMBER = 'member'

    def __str__(self) -> str:
        return self.value

    def to_lightdash_expression(self) -> ProjectMemberRole:
        """Convert to lightdash role"""
        return ProjectMemberRole(self.value)


class ProjectMember(LightdashUser):
    """Information about a Lightdash project member"""
    role: ProjectRole = Field(description='Member role')
    expired_on: FutureDate = Field(description='Member expired on', default=None)

    def is_expired(self) -> bool:
        """Check if the member is expired"""
        today = datetime.date.today()
        if is_future_date(today, self.expired_on):
            return False
        return True

    # pylint: disable=no-self-argument,no-self-use
    @validator('expired_on')
    def validate_expired_on(cls, v):
        """expired_on must be in the expiration days"""
        settings = get_settings()
        role_expiration_days = settings.ROLE_EXPIRATION_DAYS
        if (settings.CHECK_ROLE_EXPIRATION is True
                and v > datetime.date.today() + datetime.timedelta(days=role_expiration_days)):
            raise ValidationError(f'expired_on must be in {role_expiration_days} days')
        return v

    def __eq__(self, other) -> bool:
        """Compare with another ProjectMember"""
        if not isinstance(other, ProjectMember):
            raise ValueError("Can't compare with a non ProjectMember")
        if self.email == other.email and self.role == other.role and self.expired_on == other.expired_on:
            return True
        return False
