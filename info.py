#!/bin/python3
"""
Print information about a song
"""

from common import USFParser, beatsinms, getsongsdir
from typing import IO
from pathlib import PurePath
import sys, argparse

def info(filename: str | PurePath, events: bool, sec: bool, outfile: IO[str] = sys.stdout):
    parser = USFParser()
    try:
        parser.parsefile(filename)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return
    if not events:
        print(parser, file=outfile)
        return
    if events:
        try: gap = float(parser.header["gap"])
        except: gap = 0
        bpm = float(parser.header["bpm"])
        print("Type Start  Length Pitch Text", file=outfile)
        for event in parser.events:
            start = f"{(gap+beatsinms(event.start, bpm))/1000:.2f}" if sec else f"{event.start}"
            length = f"{beatsinms(event.duration, bpm)/1000:.2f}" if sec else f"{event.duration}"
            outline = f"{event.type.value:<4} {start:<5}  {length:<6} {event.pitch:<5} {event.text}"
            print(outline, file=outfile)

def main():
    ap = argparse.ArgumentParser(description="print information about a song to stdout")
    ap.add_argument("file", help="song txt file")
    ap.add_argument("-e", "--events", help="list events", action="store_true")
    ap.add_argument("-s", "--sec", help="display times as seconds instead of beats", action="store_true")
    ap.add_argument("-r", "--relative", help="interpret file path as relative to songs dir (if defined via config)", action="store_true")
    args = ap.parse_args()
    filename = args.file
    if args.relative:
        try:
            songsdir = PurePath(getsongsdir())
        except:
            print("songs dir must be defined when using -r!")
            return
        filename = songsdir.joinpath(filename)
    info(filename, args.events, args.sec)

if __name__ == "__main__":
    main()
