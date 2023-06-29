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
