from functools import lru_cache

from pydantic import BaseSettings, Field


class LightdashOpsSettings(BaseSettings):
    """Global settings

    NOTE Pydantic enables us to parse environment variables.

    SEE https://docs.pydantic.dev/latest/usage/settings/
    """
    LIGHTDASH_BASE_URL: str = Field(default='https://app.lightdash.cloud',
                                    qdescription='Lightdash base URL',
                                    env='LIGHTDASH_BASE_URL')
    LIGHTDASH_CLIENT_TIMEOUT: float = Field(default=5.0,
                                            qdescription='Lightdash base URL',
                                            env='LIGHTDASH_CLIENT_TIMEOUT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Singleton
@lru_cache(maxsize=None)
def get_settings(**kwargs) -> LightdashOpsSettings:
    """Get the settings as a singleton

    SEE https://fastapi.tiangolo.com/es/advanced/settings/#creating-the-settings-only-once-with-lru_cache
    """
    return LightdashOpsSettings(**kwargs)
