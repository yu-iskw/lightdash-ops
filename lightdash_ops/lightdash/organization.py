from typing import List

from lightdash_client import AuthenticatedClient
from lightdash_client.api.organizations import (get_my_organization,
                                                list_organization_members,
                                                list_organization_projects)
from lightdash_client.api.roles_permissions import update_organization_member
from lightdash_client.models import (
    GetMyOrganizationResponse200, GetMyOrganizationResponse200Results,
    ListOrganizationMembersResponse200,
    ListOrganizationMembersResponse200ResultsItem,
    ListOrganizationProjectsResponse200,
    ListOrganizationProjectsResponse200ResultsItem,
    UpdateOrganizationMemberJsonBody, UpdateOrganizationMemberJsonBodyRole,
    UpdateOrganizationMemberResponse200)
from lightdash_client.types import Response

from lightdash_ops.models.organization import OrganizationRole


def get_organization(
        client: AuthenticatedClient
) -> GetMyOrganizationResponse200Results:
    """Get the current client's organization"""
    response: Response[GetMyOrganizationResponse200] = get_my_organization.sync_detailed(client=client)
    return response.parsed.results  # type: ignore[union-attr]


def get_projects(
        client: AuthenticatedClient
) -> List[ListOrganizationProjectsResponse200ResultsItem]:
    """Get all project of the current user's organization

    SEE https://github.com/lightdash/lightdash/issues/5905
    """
    response: Response[ListOrganizationProjectsResponse200] = list_organization_projects.sync_detailed(client=client)
    return response.parsed.results  # type: ignore[union-attr]


def get_organization_members(
        client: AuthenticatedClient
) -> List[ListOrganizationMembersResponse200ResultsItem]:
    """Gets all the members of the organization"""
    response: Response[ListOrganizationMembersResponse200] = list_organization_members.sync_detailed(client=client)
    return response.parsed.results  # type: ignore[union-attr]


def update_organization_member_role(
        client: AuthenticatedClient,
        user_uuid: str,
        role: OrganizationRole,
) -> Response[UpdateOrganizationMemberResponse200]:
    """Update a user's access to the organization"""
    body = UpdateOrganizationMemberJsonBody(role=UpdateOrganizationMemberJsonBodyRole(role.value))
    response: Response[UpdateOrganizationMemberResponse200] = update_organization_member.sync_detailed(
        client=client, user_uuid=user_uuid, json_body=body)
    return response  # type: ignore[union-attr]
