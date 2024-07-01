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

import textwrap

import click

from lightdash_ops.cli.exposures import exposures_app
from lightdash_ops.cli.organization_v1 import organization_app
from lightdash_ops.models.settings import get_settings


def recursive_help(cmd, parent=None, depth=1):
    ctx = click.core.Context(cmd, info_name=cmd.name, parent=parent)
    head_element = '#' * depth
    command_doc = textwrap.dedent(f"""
    {head_element} {cmd.name}

    {textwrap.dedent(cmd.get_help(ctx))}

    """
    ).lstrip()
    print(command_doc)
    commands = getattr(cmd, 'commands', {})
    for sub in commands.values():
        recursive_help(sub, ctx, depth + 1)


@click.group('main')
def app():
    pass


@app.command('dump-help')
def dump_help():
    """Recursively dump the help of all commands."""
    recursive_help(app)


@app.command('dump-settings')
def dump_settings():
    """Dump the settings of the CLI."""
    settings = get_settings()
    for k, v in settings.model_dump().items():
        print(f'{k}={v}')


app.add_command(organization_app, name='organization')
app.add_command(exposures_app, name='exposures')

if __name__ == '__main__':
    app()
