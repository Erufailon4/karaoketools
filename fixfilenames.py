#!/bin/python3
"""
Change the file names in (and of) the txt file to match the song title and artist
"""

from common import USFParser, getsongsdir, getmaterialsdir
from pathlib import PurePath, Path
import argparse, os, shutil

def fixfilenames(filename, songsdir, materialsdir=None):
    parser = USFParser()
    parser.parsefile(filename)
    song = parser.header["title"]
    artist = parser.header["artist"]
    newname = f"{artist} - {song}"
    if materialsdir is not None: materialfiles = []
    for header in ["mp3", "cover", "background", "video"]:
        if header in parser.header:
            if materialsdir is not None: oldfile = parser.header[header]
            filenameparts = parser.header[header].rsplit(sep='.', maxsplit=1)
            parser.modifyheader(header, newname+"."+filenameparts[1])
            if materialsdir is not None: materialfiles.append((oldfile, parser.header[header]))
    if not Path(songsdir.joinpath(newname)).is_dir():
        os.mkdir(songsdir.joinpath(newname))
    parser.encodetofile(songsdir.joinpath(newname, newname+".txt"))
    if materialsdir is not None:
        for file in materialfiles:
            if Path(materialsdir.joinpath(file[0])).is_file():
                shutil.copyfile(materialsdir.joinpath(file[0]), songsdir.joinpath(newname, file[1]))

def main():
    ap = argparse.ArgumentParser(description="change the file names in (and of) the txt file to match the song title and artist")
    ap.add_argument("file", help="txt file to change")
    ap.add_argument("-s", "--songsdir", help="songs directory (default: from config if set, otherwise immediate parent of file)")
    ap.add_argument("-r", "--relative", help="interpret file path as relative to songs dir (if songs dir defined via -s or config)", action="store_true")
    ap.add_argument("-c", "--copy", help="copy mentioned files to the new directory (if materials dir defined via config)", action="store_true")
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
    materialsdir = None
    if args.copy:
        try:
            materialsdir = PurePath(getmaterialsdir())
        except Exception as e:
            print("materials dir must be defined when using -c!")
            print(e)
            return
    fixfilenames(filepath, songsdir, materialsdir)

if __name__ == "__main__":
    main()
