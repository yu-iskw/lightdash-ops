import os
import unittest

from lightdash_ops.models.settings import LightdashOpsSettings


class TestManagerSettings(unittest.TestCase):

    def test_set_by_env_vars(self):
        # Configure the settings by env vars
        os.environ['LIGHTDASH_BASE_URL'] = 'http://localhost:8000'
        os.environ['LIGHTDASH_CLIENT_TIMEOUT'] = '1'

        # Create the settings
        settings = LightdashOpsSettings()
        self.assertEqual(settings.LIGHTDASH_BASE_URL, 'http://localhost:8000')
        self.assertEqual(settings.LIGHTDASH_CLIENT_TIMEOUT, 1)
