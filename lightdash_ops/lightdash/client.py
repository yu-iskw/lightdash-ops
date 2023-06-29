from lightdash_client import AuthenticatedClient


def get_lightdash_client(
        api_key: str,
        timeout: float = 5.0,
        base_url='https://app.lightdash.cloud') -> AuthenticatedClient:
    """Get a test client for the Lightdash API

    The function is used to skip tests that require a valid API key.
    """
    client = AuthenticatedClient(base_url=base_url, token=api_key, timeout=timeout)
    return client  # type: ignore
