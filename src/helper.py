import geopandas as gp
from geopandas import GeoDataFrame


def load_tiles(dir_):
    tiles = gp.read_file(dir_)
    return tiles


def load_target(dir_):
    target = gp.read_file(dir_)
    return target


def save_overlap(path: str, tiles_df: GeoDataFrame, driver='GeoJSON'):
    tiles_df.to_file(path, driver=driver)


def pprint(text, verbose=False):
    if verbose:
        print(text)
