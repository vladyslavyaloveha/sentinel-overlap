import geopandas as gp

from geopandas import GeoDataFrame
from src.helper import pprint


def _get_intersect_tiles(target: GeoDataFrame, tiles: GeoDataFrame, limit=0.001):
    # Get the indices of the tiles that are likely to be inside the bounding box of the given Polygon
    tiles_indexes = list(tiles.sindex.intersection(target.geometry[0].bounds))
    tiles = tiles.loc[tiles_indexes]
    # Make the precise tiles in Polygon query
    tiles = tiles.loc[tiles.intersects(target.geometry[0])]
    # change geometry and calculate intersection area
    target['geometry'] = target.geometry.to_crs({'init': 'epsg:6933'})
    tiles['geometry'] = tiles.geometry.to_crs({'init': 'epsg:6933'})
    tiles['area'] = tiles.geometry.apply(lambda g: g.intersection(target.geometry[0]).area / 1e6)
    tiles = tiles.loc[tiles['area'] > limit]
    tiles = tiles.sort_values(by=['area', 'Name'], ascending=[False, True])
    return tiles


def overlap(target: GeoDataFrame, tiles: GeoDataFrame, verbose):
    pprint(f"Start finding overlapping tiles", verbose)
    tiles = _get_intersect_tiles(target, tiles)

    result_tiles = list()
    for row in tiles.itertuples():
        start_area = target.geometry[0].area
        target.geometry[0] = target.geometry[0].difference(row.geometry)
        if start_area != target.geometry[0].area:
            result_tiles.append(dict(Name=row.Name, geometry=row.geometry))

    result = gp.GeoDataFrame(result_tiles, crs={'init': 'epsg:6933'})
    result = result.to_crs({'init': 'epsg:4326'})
    pprint(f"End finding overlapping tiles", verbose)

    return result


