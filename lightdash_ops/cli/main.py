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
