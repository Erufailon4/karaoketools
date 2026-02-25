#!/bin/python3
"""
Change the file names in (and of) the txt file to match the song title and artist
"""

from common import USFParser
from pathlib import PurePath
import argparse

def fixfilenames(filename):
    parser = USFParser()
    parser.parsefile(filename)
    song = parser.header["title"]
    artist = parser.header["artist"]
    newname = f"{artist} - {song}"
    for header in ["mp3", "cover", "background", "video"]:
        if header in parser.header:
            filenameparts = parser.header[header].rsplit(sep='.', maxsplit=1)
            parser.modifyheader(header, newname+"."+filenameparts[1])
    parser.encodetofile(PurePath(filename).parent.joinpath(newname+".txt"))

def main():
    ap = argparse.ArgumentParser(description="change the file names in (and of) the txt file to match the song title and artist")
    ap.add_argument("file", help="txt file to change")
    args = ap.parse_args()
    fixfilenames(args.file)

if __name__ == "__main__":
    main()
