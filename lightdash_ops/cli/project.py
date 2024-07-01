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
from lightdash_ops.operators.project_v1 import ProjectOperatorV1

logger = loguru.logger

@click.group('project')
def project_app():
    pass


@project_app.command('get-spaces')
@click.option('--project_uuid', required=True, type=str, help='The uuid of the project')
def get_spaces(project_uuid):
    """Get all spaces in a project"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = LightdashClient(
        base_url=settings.LIGHTDASH_URL,
        token=settings.LIGHTDASH_API_KEY,
    )
    # Create the operator
    operator = ProjectOperatorV1(client=client)
    # Get all spaces in the project
    spaces = operator.get_spaces(project_uuid=project_uuid)
    spaces_json = json.dumps([s.model_dump(exclude_none=True, exclude_unset=True) for s in spaces], indent=2)
    click.echo(spaces_json)


@project_app.command('get-members')
@click.option('--role', type=click.Choice([role.value for role in OrganizationRole]), help='Project role')
@click.option('--project_uuid', required=True, type=str, help='The uuid of the project')
def get_members(role, project_uuid):
    """Get members in a project as JSON"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = LightdashClient(
        base_url=settings.LIGHTDASH_URL,
        token=settings.LIGHTDASH_API_KEY,
    )
    # Create the operator
    operator = ProjectOperatorV1(client=client)
    # Get all members in the project
    members = operator.get_project_members(project_uuid=project_uuid)
    if role is not None:
        members = [member for member in members if member.role.value == role]
    # Format output
    formatted_members = [member.model_dump(exclude_none=True, exclude_unset=True) for member in members]
    click.echo(json.dumps(formatted_members, indent=2))
