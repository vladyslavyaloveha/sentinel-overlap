import json
import geopandas as gp
import requests

from geopandas import GeoDataFrame


def _get_response_from_drive(file_id, url="https://docs.google.com/uc?export=download"):
    with requests.Session() as s:
        response = s.get(url, params={'id': file_id}, stream=True)
        if response.status_code == 200:
            return response
        else:
            raise ValueError(f"Cannot get response from {url} with file_id {file_id}, "
                             f"status code {response.status_code}")


def load_from_drive(file_id, verbose):
    pprint(f"Loading GeoData for {file_id} file", verbose)
    response = _get_response_from_drive(file_id)
    loaded_data = json.loads(response.text)
    tiles = GeoDataFrame.from_features(loaded_data["features"], crs={'init': 'epsg:4326'})
    pprint(f"GeoData for loaded", verbose)
    return tiles


def load_target(dir_):
    target = gp.read_file(dir_)
    return target


def save_to_file(path: str, tiles_df: GeoDataFrame, driver='GeoJSON'):
    try:
        tiles_df.to_file(path, driver=driver)
    except Exception as e:
        print(f"Cannot save data to file: {path}, error: {str(e)}")


def pprint(text, verbose=False):
    if verbose:
        print(text)
