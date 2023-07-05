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

import json
from typing import Annotated, Optional

import loguru
import typer

from lightdash_ops.lightdash.client import get_lightdash_client
from lightdash_ops.models.project_member import ProjectRole
from lightdash_ops.models.settings import get_settings
from lightdash_ops.operators.organization_v1 import OrganizationOperatorV1
from lightdash_ops.operators.project_v1 import ProjectOperatorV1

logger = loguru.logger

project_v1_app = typer.Typer()


@project_v1_app.command('get-members')
def get_project_members(
        project_uuid: Annotated[str, typer.Option(help='Lightdash project UUID')],
):
    """Get the members of a project as JSON"""
    # Load the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)
    # Create the operator
    operator = ProjectOperatorV1(client=client)
    members = operator.get_project_members(project_uuid=project_uuid)
    print(json.dumps(members, indent=2))


@project_v1_app.command('grant-role')
def grant_project_role(
        project_uuid: Annotated[str, typer.Option(help='Lightdash project UUID')],
        role: Annotated[ProjectRole, typer.Option(help='project role')],
        user_email: Annotated[Optional[str], typer.Option(help='User email')] = None,
        user_uuid: Annotated[Optional[str], typer.Option(help='User UUID')] = None,
        dry_run: Annotated[bool, typer.Option(help='Dry run if true')] = False,
):
    # Validate inputs
    if user_email is None and user_uuid is None:
        raise typer.BadParameter('One of user_email or user_uuid must be provided')

    # Load the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)

    # Find user UUID by email
    if user_uuid is not None:
        organization_operator = OrganizationOperatorV1(client=client)
        user = organization_operator.get_organization_member_by_uuid(user_uuid=user_uuid)
        if user is not None:
            user_email = user.email
    # Check if user exists
    if user_email is None:
        raise typer.BadParameter('User not found')

    # Grant role to the user
    project_operator = ProjectOperatorV1(client=client)
    project_operator.grant_project_member_role_by_email(
        project_uuid=project_uuid,
        email=user_email,
        role=role,
        dry_run=dry_run)


@project_v1_app.command('revoke-role')
def revoke_project_role(
        project_uuid: Annotated[str, typer.Option(help='Lightdash project UUID')],
        role: Annotated[ProjectRole, typer.Option(help='project role')],
        user_email: Annotated[Optional[str], typer.Option(help='User email')] = None,
        user_uuid: Annotated[Optional[str], typer.Option(help='User UUID')] = None,
        dry_run: Annotated[bool, typer.Option(help='Dry run if true')] = False,
):
    # Validate inputs
    if user_email is None and user_uuid is None:
        raise typer.BadParameter('One of user_email or user_uuid must be provided')

    # Load the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)

    # Find user UUID by email
    if user_uuid is not None:
        organization_operator = OrganizationOperatorV1(client=client)
        user = organization_operator.get_organization_member_by_uuid(user_uuid=user_uuid)
        if user is not None:
            user_email = user.email
    # Check if user exists
    if user_email is None:
        raise typer.BadParameter('User not found')

    # Revoke role from the user
    operator = ProjectOperatorV1(client=client)
    try:
        operator.revoke_project_member_role_by_email(
            project_uuid=project_uuid, email=user_email, dry_run=dry_run)
        logger.info(f'Revoked role {role} from user {user_email}')
    # pylint: disable=broad-except
    except Exception as e:
        raise RuntimeError(f'Failed to revoke role: {e}') from e


@project_v1_app.command('get-spaces')
def get_spaces(
        project_uuid: Annotated[str, typer.Option(help='Lightdash project UUID')],
):
    """Get all spaces in a project as JSON"""
    # Load the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)
    # Create the operator
    operator = ProjectOperatorV1(client=client)
    # Get all spaces
    spaces = operator.get_spaces(project_uuid=project_uuid)
    # Format output
    formatted_spaces = []
    for s in spaces:
        formatted_spaces.append({
            'space_uuid': s.uuid,
            'name': s.name,
            'visibility': s.visibility.value,
            'members': [m.email for m in s.members],
        })
    print(json.dumps(formatted_spaces, indent=2))


@project_v1_app.command('share-space-access')
def share_space_access(
        project_uuid: Annotated[str, typer.Option(help='Lightdash project UUID')],
        space_uuid: Annotated[str, typer.Option(help='Lightdash space UUID')],
        user_uuid: Annotated[str, typer.Option(help='Lightdash user UUID')],
        user_email: Annotated[str, typer.Option(help='Lightdash user email')],
        dry_run: Annotated[bool, typer.Option(help='Dry run if true')] = False,
):
    """Share space access with another user"""
    # Load the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)

    # Find user UUID by email
    if user_uuid is not None:
        organization_operator = OrganizationOperatorV1(client=client)
        user = organization_operator.get_organization_member_by_uuid(user_uuid=user_uuid)
        if user is not None:
            user_email = user.email
    # Check if user exists
    if user_email is None:
        raise typer.BadParameter('User not found')

    # Create the operator
    operator = ProjectOperatorV1(client=client)
    # Share space access
    try:
        operator.grant_space_role(
            project_uuid=project_uuid,
            space_uuid=space_uuid,
            user_uuid=user_uuid,
            dry_run=dry_run,
        )
    # pylint: disable=broad-except
    except Exception as e:
        raise RuntimeError(f'Failed to share space access: {e}') from e


@project_v1_app.command('revoke-space-access')
def revoke_space_access(
        project_uuid: Annotated[str, typer.Option(help='Lightdash project UUID')],
        space_uuid: Annotated[str, typer.Option(help='Lightdash space UUID')],
        user_uuid: Annotated[str, typer.Option(help='Lightdash user UUID')],
        user_email: Annotated[str, typer.Option(help='Lightdash user email')],
        dry_run: Annotated[bool, typer.Option(help='Dry run if true')] = False,
):
    """Share space access with another user"""
    # Load the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)

    # Find user UUID by email
    if user_uuid is not None:
        organization_operator = OrganizationOperatorV1(client=client)
        user = organization_operator.get_organization_member_by_uuid(user_uuid=user_uuid)
        if user is not None:
            user_email = user.email
    # Check if user exists
    if user_email is None:
        raise typer.BadParameter('User not found')

    # Create the operator
    operator = ProjectOperatorV1(client=client)
    # Revoke space access
    try:
        operator.grant_space_role(
            project_uuid=project_uuid, space_uuid=space_uuid, user_uuid=user_uuid, dry_run=dry_run)
    # pylint: disable=broad-except
    except Exception as e:
        raise RuntimeError(f'Failed to revoke space access: {e}') from e
