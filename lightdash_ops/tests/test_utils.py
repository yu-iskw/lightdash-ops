import unittest
from datetime import date

from lightdash_ops.utils import get_list_differences, is_future_date, mask_text


class TestUtils(unittest.TestCase):

    def test_is_future_date(self):
        date1 = date(year=2023, month=1, day=1)
        date2 = date(year=2023, month=1, day=2)
        self.assertTrue(is_future_date(date1, date2))
        self.assertFalse(is_future_date(date2, date1))

    def test_get_list_differences(self):
        # Compare the different lists
        old_list = [1, 2, 3, None]
        new_list = [2, 3, 4]
        intersections, old_elements, new_elements = get_list_differences(
            old_list=old_list, new_list=new_list)
        self.assertEqual(intersections, [2, 3])
        self.assertEqual(old_elements, [1])
        self.assertEqual(new_elements, [4])
        # Compare the same lists
        old_list = [2, 3, 4]
        new_list = [2, 3, 4]
        intersections, old_elements, new_elements = get_list_differences(
            old_list=old_list, new_list=new_list)
        self.assertEqual(intersections, [2, 3, 4])
        self.assertEqual(old_elements, [])
        self.assertEqual(new_elements, [])

    def test_mask_text(self):
        self.assertEqual(mask_text('sample@example.com'), '****le@example****')
        self.assertEqual(mask_text('a@b.com'), '*******')
