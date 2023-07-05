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
from typing import Annotated

import loguru
import typer

from lightdash_ops.lightdash.client import get_lightdash_client
from lightdash_ops.models.organization import OrganizationRole
from lightdash_ops.models.settings import get_settings
from lightdash_ops.operators.organization_v1 import OrganizationOperatorV1

logger = loguru.logger

organization_v1_app = typer.Typer()


@organization_v1_app.command('get-projects')
def get_projects():
    """Get all projects in an organization"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)
    # Create the operator
    operator = OrganizationOperatorV1(client=client)
    # Get all projects
    projects = operator.get_projects()
    projects_json = json.dumps([p.dict() for p in projects], indent=2)
    print(projects_json)


@organization_v1_app.command('get-members')
def get_members(
        role: Annotated[OrganizationRole, typer.Option(help='project role')] = None  # type: ignore[assignment]
):
    """Get members in an organization as JSON"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)
    # Create the operator
    operator = OrganizationOperatorV1(client=client)
    # Get all members in the organization
    members = operator.get_organization_members()
    if role is not None:
        members = [member for member in members if member.role == role]
    # Format output
    formatted_members = [member.dict() for member in members]
    print(json.dumps(formatted_members, indent=2))


@organization_v1_app.command('grant-role')
def grant_member_role(
        email: Annotated[str, typer.Option(help='member email')],
        role: Annotated[OrganizationRole, typer.Option(help='project role')] = None  # type: ignore[assignment]
):
    """Grant a member a role in the organization"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = get_lightdash_client(api_key=settings.LIGHTDASH_API_KEY,
                                  base_url=settings.LIGHTDASH_URL)
    # Create the operator
    operator = OrganizationOperatorV1(client=client)
    # Grant the role to the member
    try:
        operator.update_member_role_by_email(email=email, role=role)
        logger.info(f'Granted {email} the role {role}')
    # pylint: disable=broad-except
    except Exception as e:
        logger.error(f'Failed to grant {email} the role {role}')
        logger.error(e)
