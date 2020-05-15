#!/usr/bin/env python
# coding: utf-8

import argparse
import time as t
import src.helper as h

from src.helper import pprint
from src.overlap import overlap

parser = argparse.ArgumentParser(description="Script to find Sentinel2 overlap tiles for the given region)")
parser.add_argument('-i', '--input', help="Path to target .geojson file with the given region")
parser.add_argument('-o', '--output', help="Path to output .geojson file", default="overlap.geojson")
parser.add_argument('-id', '--file_id', help="Id of file on Google Drive", default="184xXr4eq41SdBDiOOogMy2ajSjKFNT7H")
parser.add_argument('-v', '--verbose', help="verbose mode", action="store_true")

args = parser.parse_args()

dir_ = "F:/Vlad/TestTaskQuantum/"
args.input = dir_ + "kharkiv/Kharkiv_region.geojson"
args.file_id = '184xXr4eq41SdBDiOOogMy2ajSjKFNT7H'
args.output = "F:/overlap.geojson"

args.verbose = True


def main():

    tiles = h.load_from_drive(args.file_id, args.verbose)

    print(tiles)

    target = h.load_target(args.input)

    print(target)

    overlap_tiles = overlap(target, tiles, args.verbose)

    h.save_to_file(args.output, overlap_tiles)

    print(f"Found tiles:\n{', '.join(list(overlap_tiles.Name))}")


if __name__ == '__main__':
    start = t.time()
    pprint(f"Start script execution", args.verbose)
    try:
        main()
    except Exception as e:
        print(f"Got error, while script was working: {str(e)}")
    pprint(f"Finished execution at {t.strftime('%H:%M:%S', t.gmtime(t.time() - start))}", args.verbose)
