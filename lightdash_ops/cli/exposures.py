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

import os
import shutil
from typing import List, Tuple

import click
import loguru

from lightdash_ops.lightdash.v1.client import LightdashClient
from lightdash_ops.models.settings import get_settings
from lightdash_ops.operators.exposures_v1 import DbtExposuresOperatorV1
from lightdash_ops.utils import dump_yaml

logger = loguru.logger


def get_default_exposure_types():
    return ['dashboard']


@click.group('exposures')
def exposures_app():
    pass


@exposures_app.command('generate-all')
@click.option(
    '--exposure_types',
    required=False,
    type=str,
    multiple=True,
    help='The types of exposures to generate',
    default=get_default_exposure_types(),
)
@click.option(
    '--output',
    required=True,
    type=str,
    help='The path to the output directory',
)
@click.option(
    '--project_names',
    required=False,
    type=str,
    multiple=True,
    help='The names of the projects to generate exposures for',
    default=None,
)
@click.option(
    '--overwrite',
    required=False,
    type=bool,
    help='Overwrite the output file',
    default=False,
)
def generate_all(exposure_types: Tuple[str], output: str, project_names: Tuple[str], overwrite: bool):
    """Generate dbt Exposures of all Lightdash projects"""
    # Get the settings
    settings = get_settings()

    # Make sure the output file exists
    if overwrite and os.path.exists(output):
        # Recursively remove the directory
        if os.path.isfile(output):
            os.remove(output)
        elif os.path.isdir(output):
            shutil.rmtree(output)
    os.makedirs(output, exist_ok=True)

    # Create the Lightdash client
    client = LightdashClient(
        base_url=settings.LIGHTDASH_URL,
        token=settings.LIGHTDASH_API_KEY,
    )
    # Create the operator
    operator = DbtExposuresOperatorV1(client=client)
    # Get dbt exposures for each project
    exposures_in_all_projects = operator.get_dbt_exposures_in_all_projects(
        exposure_types=list(exposure_types),
        project_names=list(project_names),
    )
    # Dump to yaml
    errors = []
    for project_name, exposures in exposures_in_all_projects.items():
        click.echo(f'Exporting the Project {project_name}')
        output_file = os.path.join(output, f'{project_name}.yaml')
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml_output = dump_yaml(exposures.model_dump(exclude_none=True))
                f.write(yaml_output)
        # pylint: disable=broad-except
        except Exception as e:
            errors.append(e)
    # Print errors
    for error in errors:
        click.echo(f'Error: {error}')


@exposures_app.command('generate')
@click.option(
    '--project_uuid',
    required=True,
    type=str,
    help='The uuid of the project to generate exposures for',
)
@click.option(
    '--exposure_types',
    required=False,
    type=str,
    multiple=True,
    help='The types of exposures to generate',
    default=get_default_exposure_types(),
)
def generate(project_uuid: str, exposure_types: List[str]):
    """Get all projects in an organization"""
    # Get the settings
    settings = get_settings()
    # Create the Lightdash client
    client = LightdashClient(
        base_url=settings.LIGHTDASH_URL,
        token=settings.LIGHTDASH_API_KEY,
    )
    # Create the operator
    operator = DbtExposuresOperatorV1(client=client)
    # Get dbt exposures for each project
    exposures = operator.get_dbt_exposures_in_project(
        project_uuid=project_uuid, exposure_types=exposure_types
    )
    # Dump to yaml
    yaml_output = dump_yaml(exposures.model_dump(exclude_none=True))
    print(yaml_output)
