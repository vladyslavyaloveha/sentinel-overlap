import json
import os.path
import unittest
from unittest import mock
from unittest.mock import patch

import geopandas as gp
from geopandas import GeoDataFrame

from overlap.helper import (
    _get_response_from_drive,
    load_from_drive,
    save_to_file,
    load_from_file, )


class LoadFromDriveTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_session_patcher = patch('overlap.helper.requests.Session')
        self.mock_session = self.mock_session_patcher.start()
        # Configure the mock get in the session
        self.mock_get = self.mock_session.return_value.__enter__.return_value.get
        self.status_code = 200
        self.file_id = "mock_id"
        self.path = "test_subset_sentinel2_tiles.geojson"

    def tearDown(self):
        self.mock_session_patcher.stop()

    def test_get_response_from_drive(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value = mock.MagicMock(self.status_code)
        response = _get_response_from_drive(self.file_id)
        self.assertEqual(response.status_code, self.status_code)

    def test_load_from_drive(self):
        sentinel_subset = self.__json_load()
        # Configure the mock to return a response with an OK status code and test data.
        self.mock_get.return_value = mock.MagicMock(status_code=self.status_code,
                                                    text=json.dumps(sentinel_subset))

        expected = GeoDataFrame.from_features(sentinel_subset["features"],
                                              crs={'init': 'epsg:4326'})
        actual = load_from_drive(self.file_id, False)
        assert expected.equals(actual)

    def __json_load(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
            return data


class IOTestCase(unittest.TestCase):
    def setUp(self):
        self.kh_path = "../Kharkiv_region.geojson"
        self.k_path = "Kyiv.geojson"

    def test_load_from_file(self):
        expected = gp.read_file(self.kh_path)
        actual = load_from_file(self.kh_path)
        assert expected.equals(actual)

    def test_save_to_file(self):
        path = "test_Kyiv.geojson"
        kyiv_df = gp.read_file(self.k_path, driver='GeoJSON')
        save_to_file(path, kyiv_df)
        assert os.path.isfile(path)
        os.remove(path)

