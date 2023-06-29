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
