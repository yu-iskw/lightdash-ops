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

from typing import List

from lightdash_client import AuthenticatedClient
from lightdash_client.api.roles_permissions import (
    get_project_access_list, grant_project_access_to_user,
    revoke_project_access_for_user, update_project_access_for_user)
from lightdash_client.models import (
    GetProjectAccessListResponse200,
    GetProjectAccessListResponse200ResultsItem,
    GrantProjectAccessToUserJsonBody, GrantProjectAccessToUserJsonBodyRole,
    GrantProjectAccessToUserResponse200, RevokeProjectAccessForUserResponse200,
    UpdateProjectAccessForUserJsonBody, UpdateProjectAccessForUserJsonBodyRole,
    UpdateProjectAccessForUserResponse200)
from lightdash_client.types import Response

from lightdash_ops.models.project_member import ProjectRole


def get_project_members(
        client: AuthenticatedClient,
        project_uuid: str
) -> List[GetProjectAccessListResponse200ResultsItem]:
    """Gets all the members of the organization"""
    response: Response[GetProjectAccessListResponse200] = get_project_access_list.sync_detailed(
        client=client, project_uuid=project_uuid)
    return response.parsed.results  # type: ignore[union-attr]


def update_project_member_role(
        client: AuthenticatedClient,
        project_uuid: str,
        user_uuid: str,
        role: ProjectRole,
) -> Response[UpdateProjectAccessForUserResponse200]:
    """Update a user's access to a project"""
    body = UpdateProjectAccessForUserJsonBody(role=UpdateProjectAccessForUserJsonBodyRole(role.value))
    response: Response[UpdateProjectAccessForUserResponse200] = update_project_access_for_user.sync_detailed(
        client=client, project_uuid=project_uuid, user_uuid=user_uuid, json_body=body)
    return response


def grant_project_member_role(
        client: AuthenticatedClient,
        project_uuid: str,
        email: str,
        role: ProjectRole,
) -> Response[GrantProjectAccessToUserResponse200]:
    """Grant a user access to a project"""
    # SEE https://github.com/lightdash/lightdash/pull/5907
    body = GrantProjectAccessToUserJsonBody(
        send_email=False,
        email=email,
        role=GrantProjectAccessToUserJsonBodyRole(role.value),
    )
    response: Response[GrantProjectAccessToUserResponse200] = grant_project_access_to_user.sync_detailed(
        client=client, project_uuid=project_uuid, json_body=body)
    return response  # type: ignore[assignment]


def revoke_project_access(
        client: AuthenticatedClient,
        project_uuid: str,
        user_uuid: str,
) -> Response[RevokeProjectAccessForUserResponse200]:
    """Revoke a user's access to a project"""
    response: Response[RevokeProjectAccessForUserResponse200] = revoke_project_access_for_user.sync_detailed(
        client=client, project_uuid=project_uuid, user_uuid=user_uuid)
    return response
