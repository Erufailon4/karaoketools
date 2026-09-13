#!/bin/python3
"""
Output a CSV dataset of the notes in a song for statistics and analysis
"""

from common import USFParser, getsongsdir
from common import USFEventType as UET
from pathlib import PurePath
from typing import IO
import csv, argparse

def statsfile(infile: str | PurePath, outfile: str | PurePath, ignorepitchless: bool = True):
    parser = USFParser()
    try:
        parser.parsefile(infile)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return
    linenum = 1
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["line","pitch","length"])
        for event in parser.events:
            if event.type == UET.ENDOFPHRASE:
                linenum += 1
                continue
            if event.type == UET.EOF or (ignorepitchless and event.type in [UET.FREESTYLE, UET.RAP, UET.RAPGOLDEN]):
                continue
            writer.writerow([linenum, event.pitch, event.duration])

# https://github.com/UltraStar-Deluxe/format/blob/main/The%20UltraStar%20File%20Format%20%28Unversioned%29.md#41-notes

def main():
    ap = argparse.ArgumentParser(description="output a CSV dataset of the notes in a song for statistics and analysis")
    ap.add_argument("infile", help="song txt file")
    ap.add_argument("outfile", help="output csv file")
    ap.add_argument("-r", "--relative", help="interpret input file path as relative to songs dir (if defined via config)", action="store_true")
    args = ap.parse_args()
    filename = args.infile
    if args.relative:
        try:
            songsdir = PurePath(getsongsdir())
        except:
            print("songs dir must be defined when using -r!")
            return
        filename = songsdir.joinpath(filename)
    statsfile(filename, args.outfile)

if __name__ == "__main__":
    main()
