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
from lightdash_client.api.projects import list_spaces_in_project
from lightdash_client.api.roles_permissions import (
    add_space_share_to_user, create_space_in_project,
    revoke_space_access_for_user)
from lightdash_client.api.roles_permissions import \
    update_space as update_space_api
from lightdash_client.api.spaces import delete_space
from lightdash_client.api.spaces import get_space as get_space_api
from lightdash_client.models import (AddSpaceShareToUserJsonBody,
                                     AddSpaceShareToUserResponse200,
                                     CreateSpaceInProjectJsonBody,
                                     CreateSpaceInProjectResponse200,
                                     DeleteSpaceResponse204,
                                     GetSpaceResponse200,
                                     GetSpaceResponse200Results,
                                     ListSpacesInProjectResponse200,
                                     ListSpacesInProjectResponse200ResultsItem,
                                     RevokeSpaceAccessForUserResponse200,
                                     UpdateSpaceJsonBody,
                                     UpdateSpaceResponse200)
from lightdash_client.types import Response


def create_space(
        client: AuthenticatedClient,
        project_uuid: str,
        name: str,
        is_private: bool = True) -> Response[CreateSpaceInProjectResponse200]:
    """Create a space in a project"""
    body = CreateSpaceInProjectJsonBody(name=name, is_private=is_private)
    response: Response[CreateSpaceInProjectResponse200] = create_space_in_project.sync_detailed(
        client=client, project_uuid=project_uuid, json_body=body)
    return response


def update_space(
        client: AuthenticatedClient,
        project_uuid: str,
        space_uuid: str,
        name: str,
        is_private: bool,
) -> Response[UpdateSpaceResponse200]:
    """Update a space in a project"""
    body = UpdateSpaceJsonBody(name=name, is_private=is_private)
    response: Response[UpdateSpaceResponse200] = update_space_api.sync_detailed(
        client=client, project_uuid=project_uuid, space_uuid=space_uuid, json_body=body)
    return response


def delete_space_by_uuid(
        client: AuthenticatedClient,
        project_uuid: str,
        space_uuid: str
) -> Response[DeleteSpaceResponse204]:
    """Delete a space in a project"""
    response: Response[DeleteSpaceResponse204] = delete_space.sync_detailed(
        client=client, project_uuid=project_uuid, space_uuid=space_uuid)
    return response


def get_spaces(
        client: AuthenticatedClient,
        project_uuid: str
) -> List[ListSpacesInProjectResponse200ResultsItem]:
    """Get all spaces in a project"""

    response: Response[ListSpacesInProjectResponse200] = list_spaces_in_project.sync_detailed(
        client=client, project_uuid=project_uuid)
    return response.parsed.results  # type: ignore[return-value,union-attr]


def get_space(
        client: AuthenticatedClient,
        project_uuid: str, space_uuid: str
) -> GetSpaceResponse200Results:
    """Get a space in a project"""
    response: Response[GetSpaceResponse200] = get_space_api.sync_detailed(
        client=client, project_uuid=project_uuid, space_uuid=space_uuid)
    return response.parsed  # type: ignore[return-value,union-attr]


def grant_space_role(
        client: AuthenticatedClient,
        project_uuid: str,
        space_uuid: str,
        user_uuid: str,
) -> Response[AddSpaceShareToUserResponse200]:
    """Share a space with a user"""
    body = AddSpaceShareToUserJsonBody(user_uuid=user_uuid)
    response: Response[AddSpaceShareToUserResponse200] = add_space_share_to_user.sync_detailed(
        client=client, project_uuid=project_uuid, space_uuid=space_uuid, json_body=body)
    return response


def revoke_space_role(
        client: AuthenticatedClient,
        project_uuid: str,
        space_uuid: str,
        user_uuid: str,
) -> Response[RevokeSpaceAccessForUserResponse200]:
    """Revoke a user's access to a space"""
    response: Response[RevokeSpaceAccessForUserResponse200] = revoke_space_access_for_user.sync_detailed(
        client=client, project_uuid=project_uuid, space_uuid=space_uuid, user_uuid=user_uuid)
    return response
