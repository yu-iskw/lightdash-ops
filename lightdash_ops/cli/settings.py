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

from lightdash_ops.models.settings import get_settings

manager_settings_app = typer.Typer()


@manager_settings_app.command('get')
def get():
    """Get the manager settings

    NOTE:
        The output format isn't fully compatible with .env file.
    """
    settings = get_settings()
    for k, v in settings.dict().items():
        print(f'{k}={v}')
