#!/bin/python3
"""
Remove trailing hyphens from karaoke files
"""

from common import linesfromfile, writetofile, getsongsdir
import argparse
from pathlib import PurePath

def removehyphens(filename):
    lines = linesfromfile(filename)
    newlines = []
    for line in lines:
        if len(line) > 7 and line.rfind('-') != -1 and (len(line) - line.rfind('-')) < 4:
            i = line.rfind('-')
            newline = line[:i] + line[i+1:]
        else:
            newline = line
        newlines.append(newline)
    writetofile(filename, "\n".join(newlines))

def main():
    ap = argparse.ArgumentParser(description="remove trailing hyphens from karaoke files")
    ap.add_argument("file", help="txt file to remove hyphens from")
    ap.add_argument("-r", "--relative", help="interpret file path as relative to songs dir (if defined via config)", action="store_true")
    args = ap.parse_args()
    filename = args.file
    if args.relative:
        try:
            filename = PurePath(getsongsdir()).joinpath(args.file)
        except:
            print("songs dir must be defined when using -r!")
            return
    removehyphens(filename)

if __name__ == "__main__":
    main()
