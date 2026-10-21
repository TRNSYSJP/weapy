import io
import struct
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


class HeaderTest(unittest.TestCase):
    def _read_header(self, ea_no, entity_number, year):
        wea = Wea2File.__new__(Wea2File)
        wea.read_header(io.BytesIO(struct.pack('<hhh', ea_no, entity_number, year)))
        return wea

    def test_header_values_are_read(self):
        wea = self._read_header(3630, 0, 1120)
        self.assertEqual((wea.header.ea_no, wea.header.entity_number, wea.header.year), (3630, 0, 1120))

    def test_header_is_not_shared_between_instances(self):
        # The values used to be assigned to the header class, so the last file read
        # overwrote the header of every other instance.
        tokyo = self._read_header(3630, 0, 1120)
        self._read_header(20, 0, 110)
        self.assertEqual((tokyo.header.ea_no, tokyo.header.year), (3630, 1120))


class StationNameTest(unittest.TestCase):
    def _file_with_station(self):
        wea = Wea2File.__new__(Wea2File)
        wea.station = SimpleNamespace(name_jp='東京', name_roman='TOKYO')
        return wea

    def test_deprecated_station_name_returns_japanese_name(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self._file_with_station().station_name, '東京')

    def test_deprecated_station_roman_name_returns_roman_name(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self._file_with_station().station_roman_name, 'TOKYO')


if __name__ == "__main__":
    unittest.main()
