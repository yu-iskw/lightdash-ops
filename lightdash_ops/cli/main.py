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

import typer

from lightdash_ops.cli.organization_v1 import organization_v1_app
from lightdash_ops.cli.project_v1 import project_v1_app
from lightdash_ops.cli.settings import manager_settings_app

app = typer.Typer()

app.add_typer(manager_settings_app, name='settings')
app.add_typer(organization_v1_app, name='organization')
app.add_typer(project_v1_app, name='project')

if __name__ == '__main__':
    app()
