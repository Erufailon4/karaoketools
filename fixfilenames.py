#!/bin/python3
"""
Change the file names in (and of) the txt file to match the song title and artist
"""

from common import USFParser
from pathlib import PurePath
import argparse

def fixfilenames(filename, songsdir):
    parser = USFParser()
    parser.parsefile(filename)
    song = parser.header["title"]
    artist = parser.header["artist"]
    newname = f"{artist} - {song}"
    for header in ["mp3", "cover", "background", "video"]:
        if header in parser.header:
            filenameparts = parser.header[header].rsplit(sep='.', maxsplit=1)
            parser.modifyheader(header, newname+"."+filenameparts[1])
    parser.encodetofile(songsdir.joinpath(newname, newname+".txt"))

def main():
    ap = argparse.ArgumentParser(description="change the file names in (and of) the txt file to match the song title and artist")
    ap.add_argument("file", help="txt file to change")
    ap.add_argument("-s", "--songsdir", help="songs directory (default: from config if set, otherwise immediate parent of file)")
    args = ap.parse_args()
    if args.songsdir:
        songsdir = PurePath(args.songsdir)
    else:
        try:
            songsdir = PurePath(getsongsdir())
        except:
            songsdir = PurePath(args.file).parent
    fixfilenames(args.file, songsdir)

if __name__ == "__main__":
    main()
