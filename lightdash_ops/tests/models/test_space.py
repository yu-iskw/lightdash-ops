import unittest

from lightdash_ops.models.space import Space, SpaceVisibility


class TestSpace(unittest.TestCase):

    def test_invalid_visibility(self):
        # We don't allow to make a private space managed by hand.
        name = 'Test Space'
        description = 'test space'
        visibility = SpaceVisibility.PRIVATE
        allow_manual_management = True
        with self.assertRaises(ValueError):
            Space(name=name,
                  description=description,
                  visibility=visibility,
                  allow_manual_management=allow_manual_management)
