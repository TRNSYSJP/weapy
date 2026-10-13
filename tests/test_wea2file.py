import unittest
from types import SimpleNamespace

from weapy.wea2file import Wea2File


class ElevationTest(unittest.TestCase):
    def _file_with_elevation(self, elevation_m):
        # The reader stores the header's elevation as read from the file (metres);
        # build the object directly so the test needs no .wea2 data file.
        wea = Wea2File.__new__(Wea2File)
        wea.location = SimpleNamespace(elevation=elevation_m)
        return wea

    def test_elevation_is_returned_in_metres(self):
        # Nobeyama is 1,350 m; the file stores 1350 and the property must not scale it.
        self.assertEqual(self._file_with_elevation(1350).elevation, 1350)

    def test_low_elevation_is_not_divided_by_ten(self):
        # Tokyo is 25 m in the standard weather file.
        self.assertEqual(self._file_with_elevation(25).elevation, 25)


if __name__ == "__main__":
    unittest.main()
