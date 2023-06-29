import unittest

from lightdash_ops.lightdash.organization import get_projects
from lightdash_ops.lightdash.project import get_project_members
from lightdash_ops.tests.utils import get_test_client, has_lightdash_api_key


class TestLightdashOrganization(unittest.TestCase):

    def setUp(self) -> None:
        self.client = get_test_client()

    @unittest.skipIf(not has_lightdash_api_key(), 'LIGHTDASH_API_KEY environment variable not set')
    def test_get_project_members(self):
        projects = get_projects(client=self.client)
        for project in projects:
            members = get_project_members(client=self.client, project_uuid=project.project_uuid)
            if len(members) > 0:
                self.assertIsNotNone(members[0].email)
                self.assertIsNotNone(members[0].role)
