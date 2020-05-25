import geopandas as gp

from geopandas import GeoDataFrame
from overlap.helper import pprint


def _get_epsg_code(longitude: float, latitude: float):
    """
    Find all tiles that intersects given region with area >= limit km2 using R-tree indexing
        Parameters
        ----------
        longitude: float
        latitude: float

        Returns
        -------
        int
            EPSG code for current UTM Zone
    """

    def _zone_number(lat, lon):
        if 56 <= lat < 64 and 3 <= lon < 12:
            return 32
        if 72 <= lat <= 84 and lon >= 0:
            if lon < 9:
                return 31
            elif lon < 21:
                return 33
            elif lon < 33:
                return 35
            elif lon < 42:
                return 37

        return int((lon + 180) / 6) + 1

    zone = _zone_number(latitude, longitude)
    if latitude > 0:
        return 32600 + zone
    else:
        return 32700 + zone


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
    geometry = target.geometry[0]
    tiles_indexes = list(tiles.sindex.intersection(geometry.bounds))
    tiles = tiles.loc[tiles_indexes]
    # Make the precise tiles in Polygon query
    tiles = tiles.loc[tiles.intersects(geometry)]
    # change geometry and calculate intersection area
    code = _get_epsg_code(geometry.centroid.x, geometry.centroid.y)
    epsg = f"epsg:{code}"
    target['geometry'] = target.geometry.to_crs({'init': epsg})
    tiles['geometry'] = tiles.geometry.to_crs({'init': epsg})
    tiles['area'] = tiles.geometry.apply(lambda g: g.intersection(target.geometry[0]).area / 1e6)
    tiles = tiles.loc[tiles['area'] > limit]
    tiles = tiles.sort_values(by=['area', 'Name'], ascending=[False, True])
    return tiles, epsg


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
    tiles, epsg = _get_intersect_tiles(target, tiles)

    result_tiles = list()
    for row in tiles.itertuples():
        start_area = target.geometry[0].area
        target.geometry[0] = target.geometry[0].difference(row.geometry)
        if start_area != target.geometry[0].area:
            result_tiles.append(dict(Name=row.Name, geometry=row.geometry))

    result = gp.GeoDataFrame(result_tiles, crs={'init': epsg})
    result = result.to_crs({'init': 'epsg:4326'})
    pprint(f"End finding overlapping tiles", verbose)

    return result
