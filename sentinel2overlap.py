#!/usr/bin/env python
# coding: utf-8

import argparse
import time as t

import overlap as ovp
from overlap import pprint

parser = argparse.ArgumentParser(description="Script to find Sentinel2 overlap tiles for the given region)")
parser.add_argument('-i', '--input', help="Path to target .geojson file with the given region", required=True, type=str)
parser.add_argument('-o', '--output', help="Path to output .geojson file", default="overlap.geojson", type=str)
parser.add_argument('-id', '--file_id', help="Id of file on Google Drive",
                    default="184xXr4eq41SdBDiOOogMy2ajSjKFNT7H", type=str)
parser.add_argument('-v', '--verbose', help="verbose mode", action="store_true")

args = parser.parse_args()


def main():
    tiles = ovp.load_from_drive(args.file_id, args.verbose)
    target = ovp.load_from_file(args.input)

    overlap_tiles = ovp.overlap(target, tiles, args.verbose)
    print(f"Found tiles:\n{', '.join(sorted(list(overlap_tiles.Name)))}")

    pprint(f"Saving overlap tiles to {args.output} file", args.verbose)
    ovp.save_to_file(args.output, overlap_tiles)
    pprint(f"Saved overlap tiles file", args.verbose)


if __name__ == '__main__':
    start = t.time()
    pprint(f"Start script execution", args.verbose)
    try:
        main()
    except Exception as e:
        print(f"Got error, while script was working: {str(e)}")
    pprint(f"Finished execution at {t.strftime('%H:%M:%S', t.gmtime(t.time() - start))}", args.verbose)
