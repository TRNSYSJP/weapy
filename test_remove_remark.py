import unittest

from weapy.weafile import WeaFile
from weapy.wea2file import Wea2File


class RemoveRemarkTest(unittest.TestCase):
    def test_negative_value_with_remark_truncates_toward_zero(self):
        # -707 is -70.7 degC with the remark digit 7 dropped: -7.0 degC, not -7.1 degC.
        for cls in (WeaFile, Wea2File):
            self.assertEqual(cls.remove_remark(None, -707), -70, cls.__module__)

    def test_positive_and_zero_values_are_unchanged(self):
        for cls in (WeaFile, Wea2File):
            self.assertEqual(cls.remove_remark(None, 707), 70, cls.__module__)
            self.assertEqual(cls.remove_remark(None, 0), 0, cls.__module__)
            self.assertEqual(cls.remove_remark(None, -700), -70, cls.__module__)


if __name__ == "__main__":
    unittest.main()
