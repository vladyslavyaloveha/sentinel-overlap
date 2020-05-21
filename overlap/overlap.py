import geopandas as gp

from geopandas import GeoDataFrame
from overlap.helper import pprint


def _get_intersect_tiles(target: GeoDataFrame, tiles: GeoDataFrame, limit=0.001):
    """
    Find all tiles that intersects given region with area >= limit km2 using R-tree indexing
        Parameters
        ----------
        target: GeoDataFrame
            Input Polygon
        tiles: GeoDataFrame
            Tiles (Sentinel2)
        limit: float
            min considered tile area in km2
        Returns
        -------
        GeoDataFrame
            Precised intersect tiles for given Polygon
    """

    # Get the indices of the tiles that are likely to be inside the bounding box of the given Polygon
    tiles_indexes = list(tiles.sindex.intersection(target.geometry[0].bounds))
    tiles = tiles.loc[tiles_indexes]
    # Make the precise tiles in Polygon query
    tiles = tiles.loc[tiles.intersects(target.geometry[0])]
    # change geometry and calculate intersection area
    target['geometry'] = target.geometry.to_crs({'init': 'epsg:3395'})
    tiles['geometry'] = tiles.geometry.to_crs({'init': 'epsg:3395'})
    tiles['area'] = tiles.geometry.apply(lambda g: g.intersection(target.geometry[0]).area / 1e6)
    tiles = tiles.loc[tiles['area'] > limit]
    tiles = tiles.sort_values(by=['area', 'Name'], ascending=[False, True])
    return tiles


def overlap(target: GeoDataFrame, tiles: GeoDataFrame, verbose: bool):
    """
    Find all unique tiles that intersects given region, based on max coverage area
        Parameters
        ----------
        target: GeoDataFrame
            Input Polygon
        tiles: GeoDataFrame
            Tiles (Sentinel2)
        verbose: bool
            verbose mode, if True prints messages
        Returns
        -------
        GeoDataFrame
            Tiles for given Polygon
    """
    pprint(f"Start finding overlapping tiles", verbose)
    tiles = _get_intersect_tiles(target, tiles)

    result_tiles = list()
    for row in tiles.itertuples():
        start_area = target.geometry[0].area
        target.geometry[0] = target.geometry[0].difference(row.geometry)
        if start_area != target.geometry[0].area:
            result_tiles.append(dict(Name=row.Name, geometry=row.geometry))

    result = gp.GeoDataFrame(result_tiles, crs={'init': 'epsg:3395'})
    result = result.to_crs({'init': 'epsg:4326'})
    pprint(f"End finding overlapping tiles", verbose)

    return result


