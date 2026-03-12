#!/bin/python3
"""
Change the file names in (and of) the txt file to match the song title and artist
"""

from common import USFParser, getsongsdir
from pathlib import PurePath, Path
import argparse
import os

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
    if not Path(songsdir.joinpath(newname)).is_dir():
        os.mkdir(songsdir.joinpath(newname))
    parser.encodetofile(songsdir.joinpath(newname, newname+".txt"))

def main():
    ap = argparse.ArgumentParser(description="change the file names in (and of) the txt file to match the song title and artist")
    ap.add_argument("file", help="txt file to change")
    ap.add_argument("-s", "--songsdir", help="songs directory (default: from config if set, otherwise immediate parent of file)")
    ap.add_argument("-r", "--relative", help="interpret file path as relative to songs dir (if songs dir defined via -s or config)", action="store_true")
    args = ap.parse_args()
    if args.songsdir:
        songsdir = PurePath(args.songsdir)
    else:
        try:
            songsdir = PurePath(getsongsdir())
        except Exception as e:
            if args.relative:
                print("songs dir must be defined when using -r!")
                print(e)
                return
            songsdir = PurePath(args.file).parent
    filepath = args.file
    if args.relative:
        filepath = songsdir.joinpath(args.file)
    fixfilenames(filepath, songsdir)

if __name__ == "__main__":
    main()
