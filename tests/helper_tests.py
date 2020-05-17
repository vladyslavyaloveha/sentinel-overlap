import unittest
import geopandas as gp
from geopandas import GeoDataFrame
import os.path

from overlap.helper import (
    _get_response_from_drive,
    load_from_drive,
    save_to_file,
    load_from_file)


class HelperTestCase(unittest.TestCase):
    def setUp(self):
        self.file_id = "184xXr4eq41SdBDiOOogMy2ajSjKFNT7H"
        self.path = "../Kharkiv_region.geojson"

    def test_get_response_from_drive(self):
        response = _get_response_from_drive(self.file_id)
        self.assertEqual(response.status_code, 200)

    def test_load_from_drive(self):
        tiles = load_from_drive(self.file_id, False)
        self.assertIsInstance(tiles, GeoDataFrame)

    def test_load_from_file(self):
        expected = gp.read_file(self.path)
        actual = load_from_file(self.path)
        assert expected.equals(actual)

    def test_save_to_file(self):
        path = "test_Kyiv.geojson"
        kyiv_df = gp.read_file("Kyiv.geojson", driver='GeoJSON')
        save_to_file(path, kyiv_df)
        assert os.path.isfile(path)
        os.remove(path)
