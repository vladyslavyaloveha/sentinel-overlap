import time as t
import argparse

import geopandas as gp
import helper as h
from helper import pprint
import overlap

parser = argparse.ArgumentParser(description="Script to find Sentinel2 overlap tiles for the given region)")
parser.add_argument('-i', '--input', help="Path to target .geojson file with the giver region")
parser.add_argument('-o', '--output', help="Path to output .geojson file", default="overlap.geojson")
parser.add_argument('-u', '--url', help="URL to Google Drive with Sentinetel2 tiles file",
                    default="https://drive.google.com/"
                            "file/d/184xXr4eq41SdBDiOOogMy2ajSjKFNT7H/view/sentinel2_tiles.geojson")
parser.add_argument('-v', '--verbose', help="verbose mode", action="store_true")

args = parser.parse_args()

dir_ = "F:/Vlad/TestTaskQuantum/"
args.input = dir_ + "kharkiv/Kharkiv_region.geojson"
args.output = "F:/overlap.geojson"

args.verbose = True


def main():

    tiles = h.load_tiles(dir_ + "sentinel2_tiles.geojson")
    target = h.load_target(args.input)

    result_tiles = overlap.overlap(target, tiles)

    h.save_overlap(args.output, result_tiles)

    print(f"Found tiles:\n{', '.join(list(result_tiles.Name))}")


if __name__ == '__main__':
    start = t.time()
    pprint(f"Start script execution", args.verbose)
    main()
    pprint(f"Finished execution at {t.strftime('%H:%M:%S', t.gmtime(t.time() - start))}", args.verbose)
