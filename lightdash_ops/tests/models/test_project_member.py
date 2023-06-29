import unittest

from pydantic import EmailStr

from lightdash_ops.models.project_member import ProjectMember, ProjectRole


class TestProjectMember(unittest.TestCase):

    def test_valid_new(self):
        # Create the project member
        email = 'test@example.com'
        role = ProjectRole.EDITOR
        project_member = ProjectMember(email=EmailStr(email), role=role)
        self.assertEqual(project_member.email, email)
        self.assertEqual(project_member.role, role)
