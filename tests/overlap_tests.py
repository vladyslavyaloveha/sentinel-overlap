import unittest

from overlap import load_from_file, load_from_drive
from overlap.overlap import _get_intersect_tiles, overlap


class OverlapTestCase(unittest.TestCase):
    def setUp(self):
        self.target_kyiv = load_from_file("Kyiv.geojson")
        self.target_kharkiv = load_from_file("../Kharkiv_region.geojson")
        self.tiles = load_from_drive("184xXr4eq41SdBDiOOogMy2ajSjKFNT7H", False)

    def test_get_intersect_tiles(self):
        expected_name = '11SLV'
        actual_name = _get_intersect_tiles(self.target_kyiv, self.tiles).iloc[0].Name
        self.assertEqual(expected_name, actual_name)

    def test_overlap(self):
        expected_names = sorted(['36UXA', '36UXV', '36UXU', '36UYU', '36UYV',
                                 '37UCQ', '37UDQ', '37UDR', '37UCR', '36UYA', '36UYB'])
        actual_names = sorted(list(overlap(self.target_kharkiv, self.tiles, False).Name.values))

        self.assertEqual(expected_names, actual_names)
