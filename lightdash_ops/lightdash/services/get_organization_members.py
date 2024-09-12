# Copyright 2024 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.




from pydantic import BaseModel, Field

from lightdash_ops.lightdash.models.organization import OrganizationMember
from lightdash_ops.lightdash.v1.client import LightdashClient
from lightdash_ops.lightdash.v1.list_organization_members import \
    ListOrganizationMembers


class GetOrganizationMembersService(BaseModel):
    """Get all members in an organization"""
    client: LightdashClient = Field(description='The Lightdash client')

    def get_all_members(self, page_size: int = 100, include_groups: bool = False):
        members = []
        page_offset = 1
        while True:
            api_caller = ListOrganizationMembers(client=self.client)
            response = api_caller.request(page_size=page_size, page=page_offset, include_groups=include_groups)
            if not response.members:
                break
            for member in response.members:
                organization_member = OrganizationMember(
                    user_uuid=member.userUuid,
                    email=member.email,
                    role=member.role,
                    is_active=member.isActive
                )
                members.append(organization_member)
            page_offset += 1
        return members
