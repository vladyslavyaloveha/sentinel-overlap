import unittest
from collections import namedtuple

from overlap import load_from_file, load_from_drive
from overlap.overlap import (
    _get_epsg_code,
    _get_intersect_tiles,
    overlap, )


class OverlapTestCase(unittest.TestCase):
    def setUp(self):
        self.target_kyiv = load_from_file("Kyiv.geojson")
        self.target_kharkiv = load_from_file("../Kharkiv_region.geojson")
        self.tiles = load_from_drive("184xXr4eq41SdBDiOOogMy2ajSjKFNT7H", False)

    def test_get_epsg_code(self):

        kyiv = namedtuple('coordinates', ['longitude', 'latitude'])(30.5238, 50.45466)
        expected_kyiv_code = 32636
        actual_kyiv_code = _get_epsg_code(*kyiv)

        oslo = namedtuple('coordinates', ['longitude', 'latitude'])(10.74609, 59.91273)
        expected_oslo_code = 32632
        actual_oslo_code = _get_epsg_code(*oslo)

        self.assertEqual(expected_kyiv_code, actual_kyiv_code)
        self.assertEqual(expected_oslo_code, actual_oslo_code)

    def test_get_intersect_tiles(self):
        expected_names = sorted(['35UQR', '36UUA', '35UQS', '36UUB', ])
        tiles, _ = _get_intersect_tiles(self.target_kyiv, self.tiles)
        actual_names = sorted(list(tiles.Name))
        self.assertEqual(expected_names, actual_names)

    def test_overlap(self):
        expected_names = sorted(['36UXA', '36UXV', '36UXU', '36UYU', '36UYV',
                                 '37UCQ', '37UDQ', '37UDR', '37UCR', '36UYA', '36UYB', ])
        actual_names = sorted(list(overlap(self.target_kharkiv, self.tiles, False).Name.values))

        self.assertEqual(expected_names, actual_names)
