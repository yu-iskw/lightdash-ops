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

import click
import loguru

from lightdash_ops.lightdash.v1.client import LightdashClient
from lightdash_ops.models.organization import OrganizationRole
from lightdash_ops.models.settings import get_settings
from lightdash_ops.operators.organization_v1 import OrganizationOperatorV1

logger = loguru.logger

@click.group('organization')
def organization_app():
    pass


@organization_app.command('get-projects')
def get_projects():
    """Get all projects in an organization"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = LightdashClient(
        base_url=settings.LIGHTDASH_URL,
        token=settings.LIGHTDASH_API_KEY,
    )
    # Create the operator
    operator = OrganizationOperatorV1(client=client)
    # Get all projects
    projects = operator.get_projects()
    projects_json = json.dumps([p.model_dump(exclude_none=True, exclude_unset=True) for p in projects], indent=2)
    click.echo(projects_json)


@organization_app.command('get-members')
@click.option('--role', type=click.Choice([role.value for role in OrganizationRole]), help='Project role')
def get_members(role):
    """Get members in an organization as JSON"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = LightdashClient(
        base_url=settings.LIGHTDASH_URL,
        token=settings.LIGHTDASH_API_KEY,
    )
    # Create the operator
    operator = OrganizationOperatorV1(client=client)
    # Get all members in the organization
    members = operator.get_organization_members()
    if role is not None:
        members = [member for member in members if member.role.value == role]
    # Format output
    formatted_members = [member.model_dump(exclude_none=True, exclude_unset=True) for member in members]
    click.echo(json.dumps(formatted_members, indent=2))
