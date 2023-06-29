import os
from typing import Optional

from lightdash_client import AuthenticatedClient


def has_lightdash_api_key() -> bool:
    """Check if the LIGHTDASH_API_KEY environment variable is set

    The function is used to skip tests that require a valid API key.
    """
    if os.getenv('LIGHTDASH_API_KEY') is not None:
        return True
    return False


def has_lightdash_project_uuid() -> bool:
    """Check if APi key and project UUID environment variables are set"""
    if (os.getenv('LIGHTDASH_API_KEY') is not None
            and os.getenv('LIGHTDASH_PROJECT_UUID') is not None):
        return True
    return False


def get_lightdash_project_uuid() -> Optional[str]:
    """Get the LIGHTDASH_PROJECT_UUID environment variable"""
    return os.getenv('LIGHTDASH_PROJECT_UUID')


def get_test_client(base_url='https://app.lightdash.cloud',
                    api_key: str = os.getenv('LIGHTDASH_API_KEY', '')):
    """Get a test client for the Lightdash API

    The function is used to skip tests that require a valid API key.
    """
    client = AuthenticatedClient(base_url=base_url, token=api_key)
    return client
