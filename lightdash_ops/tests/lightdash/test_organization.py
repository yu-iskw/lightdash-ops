import unittest

from lightdash_ops.lightdash.organization import (get_organization_members,
                                                  get_projects)
from lightdash_ops.tests.utils import get_test_client, has_lightdash_api_key


class TestLightdashOrganization(unittest.TestCase):

    def setUp(self) -> None:
        self.client = get_test_client()

    @unittest.skipIf(not has_lightdash_api_key(), 'LIGHTDASH_API_KEY environment variable not set')
    def test_get_projects(self):
        projects = get_projects(client=self.client)
        if len(projects) > 0:
            self.assertIsNotNone(projects[0].type)
            self.assertIsNotNone(projects[0].name)
            self.assertIsNotNone(projects[0].project_uuid)

    @unittest.skipIf(not has_lightdash_api_key(), 'LIGHTDASH_API_KEY environment variable not set')
    def test_get_members(self):
        members = get_organization_members(client=self.client)
        if len(members) > 0:
            self.assertTrue(members[0].email is not None)
            self.assertTrue(members[0].user_uuid is not None)
            self.assertTrue(members[0].role is not None)
