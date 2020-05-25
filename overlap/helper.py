import json
import geopandas as gp
import requests

from geopandas import GeoDataFrame


def _get_response_from_drive(file_id: str, url="https://docs.google.com/uc?export=download"):
    """
    Load file by given filed_id and url
        Parameters
        ----------
        file_id : str
            Id of file
        url : str
            url to load, default: https://docs.google.com/uc?export=download
        Returns
        -------
        Response
            Response from url
    """

    with requests.Session() as s:
        response = s.get(url, params={'id': file_id}, stream=True)
        if response.status_code == 200:
            return response
        else:
            raise ValueError(f"Cannot get response from {url} with file_id {file_id}, "
                             f"status code {response.status_code}")


def load_from_drive(file_id: str, verbose: bool):
    """
    Load tiles by given filed_id from Google Drive
        Parameters
        ----------
        file_id : str
            Id of file on Google Drive
        verbose : bool
            verbose mode
        Returns
        -------
        GeoDataFrame
            DataFrame from loaded file
    """

    pprint(f"Loading GeoData for {file_id} file", verbose)

    response = _get_response_from_drive(file_id)
    loaded_data = json.loads(response.text)
    tiles = GeoDataFrame.from_features(loaded_data["features"], crs={'init': 'epsg:4326'})
    pprint(f"GeoData for {file_id} loaded", verbose)
    return tiles


def load_from_file(path: str):
    """
    Read from path GeoDataFrame
        Parameters
        ----------
        path : str
            full path to .geojson file
        Returns
        -------
        GeoDataFrame
            Loaded DataFrame
    """
    target = gp.read_file(path)
    return target


def save_to_file(path: str, tiles_df: GeoDataFrame, driver='GeoJSON'):
    """
    Save GeoDataFrame to given path
        Parameters
        ----------
        path : str
            path to save .geojson file
        tiles_df: GeoDataFrame
            DataFrame to save
        driver: str
            driver, default: GeoJSON
    """
    try:
        tiles_df.to_file(path, driver=driver)
    except Exception as e:
        print(f"Cannot save data to file: {path}, error: {str(e)}")


def pprint(text: str, verbose=False):
    """
    Print text, if verbose mode is used
        Parameters
        ----------
        text: str
            text to print
        verbose : bool
    """
    if verbose:
        print(text)
