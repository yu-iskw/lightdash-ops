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

from typing import List, Optional

import loguru
from lightdash_client import AuthenticatedClient
from lightdash_client.api.organizations import (create_group_in_organization,
                                                list_groups_in_organization)
from lightdash_client.api.user_groups import \
    add_user_to_group as add_lightdash_user_to_group
from lightdash_client.api.user_groups import \
    delete_group as delete_lightdash_group
from lightdash_client.api.user_groups import get_group as get_lightdash_group
from lightdash_client.api.user_groups import \
    get_group_members as get_lightdasH_group_members
from lightdash_client.api.user_groups import \
    remove_user_from_group as remove_lightdash_user_from_group
from lightdash_client.api.user_groups import \
    update_group as update_lightdash_group
from lightdash_client.models import (
    AddUserToGroupResponse200, CreateGroupInOrganizationJsonBody,
    CreateGroupInOrganizationResponse200, DeleteGroupResponse200,
    GetGroupMembersResponse200, GetGroupMembersResponse200ResultsItem,
    GetGroupResponse200, GetGroupResponse200Results,
    ListGroupsInOrganizationResponse200,
    ListGroupsInOrganizationResponse200ResultsItem,
    RemoveUserFromGroupResponse200, UpdateGroupJsonBody,
    UpdateGroupResponse200)
from lightdash_client.types import Response

logger = loguru.logger


def create_group(
        client: AuthenticatedClient,
        name: str,
) -> Response[CreateGroupInOrganizationResponse200]:
    """Creates a new group in the current user's organization"""
    body = CreateGroupInOrganizationJsonBody(name=name)
    response: Response[CreateGroupInOrganizationResponse200] = create_group_in_organization.sync_detailed(
        client=client, json_body=body)
    return response


def update_group(
        client: AuthenticatedClient,
        group_uuid: str,
        name: str,
) -> Response[UpdateGroupResponse200]:
    """Updates a group by UUID"""
    body = UpdateGroupJsonBody(name=name)
    response: Response[UpdateGroupResponse200] = update_lightdash_group.sync_detailed(
        client=client, group_uuid=group_uuid, json_body=body)
    return response


def delete_group(
        client: AuthenticatedClient,
        group_uuid: str,
) -> Response[DeleteGroupResponse200]:
    """Deletes a group by UUID"""
    response: Response[DeleteGroupResponse200] = delete_lightdash_group.sync_detailed(
        client=client, group_uuid=group_uuid)
    return response


def get_groups(
        client: AuthenticatedClient,
) -> List[ListGroupsInOrganizationResponse200ResultsItem]:
    """Get all groups in the current user's organization"""
    response: Response[ListGroupsInOrganizationResponse200] = list_groups_in_organization.sync_detailed(
        client=client)
    if response.parsed is None:
        raise ValueError('Could not get groups')
    return response.parsed.results


def get_group(
        client: AuthenticatedClient,
        group_uuid: str,
) -> Optional[GetGroupResponse200Results]:
    """Get a group by UUID"""
    response: Response[GetGroupResponse200] = get_lightdash_group.sync_detailed(
        client=client, group_uuid=group_uuid)
    if response.parsed is None:
        logger.warning('Could not get group with UUID %s', group_uuid)
        return None
    return response.parsed.results


def get_group_members(
        client: AuthenticatedClient,
        group_uuid: str,
) -> List[GetGroupMembersResponse200ResultsItem]:
    """Get all members of a group"""
    response: Response[GetGroupMembersResponse200] = get_lightdasH_group_members.sync_detailed(
        client=client, group_uuid=group_uuid)
    if response.parsed is None:
        raise RuntimeError(f'Could not get members of group with UUID {group_uuid}')
    return response.parsed.results


def add_member_to_group(
        client: AuthenticatedClient,
        group_uuid: str,
        user_uuid: str,
) -> Response[AddUserToGroupResponse200]:
    """Add a user to a group"""
    response: Response[AddUserToGroupResponse200] = add_lightdash_user_to_group.sync_detailed(
        client=client, group_uuid=group_uuid, user_uuid=user_uuid)
    return response


def remove_member_from_group(
        client: AuthenticatedClient,
        group_uuid: str,
        user_uuid: str,
) -> Response[RemoveUserFromGroupResponse200]:
    """Remove a user from a group"""
    response: Response[RemoveUserFromGroupResponse200] = remove_lightdash_user_from_group.sync_detailed(
        client=client, group_uuid=group_uuid, user_uuid=user_uuid)
    return response
