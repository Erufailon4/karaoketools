#!/bin/python3
"""
Concatenate USF files that have the same BPM
"""

from common import USFParser, USFEvent, beatsinms, msinbeats
from pathlib import PurePath
import argparse

def concat(file1: str | PurePath, file2: str | PurePath, outputfile: str | PurePath) -> None:
    parser1 = USFParser()
    parser2 = USFParser()
    try:
        parser1.parsefile(file1)
        parser2.parsefile(file2)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return
    bpm1 = float(parser1.header["bpm"])
    bpm2 = float(parser2.header["bpm"])
    if bpm1 != bpm2:
        print("BPMs must be the same!")
        return
    try:
        gap1 = float(parser1.header["gap"])
    except:
        print("No gap specified, assumed to be 0")
        gap1 = 0
    try:
        gap2 = float(parser2.header["gap"])
    except:
        print("No gap specified, assumed to be 0")
        gap2 = 0
    if gap2 >= gap1:
        former = parser1
        latter = parser2
        formergap = gap1
        lattergap = gap2
    else:
        former = parser2
        latter = parser1
        formergap = gap2
        lattergap = gap1
    gapdiff = lattergap-formergap
    former.events.append(USFEvent("E"))
    for event in latter.events:
        newstart = round(msinbeats(beatsinms(event.start, bpm1) + gapdiff, bpm1))
        newevent = event
        newevent.start = newstart
        former.events.append(newevent)
    former.encodetofile(outputfile)

def main():
    ap = argparse.ArgumentParser(description="concatenate two USF files that have the same BPM into a new file (will require manual editing afterwards)")
    ap.add_argument("file1", help="first input file")
    ap.add_argument("file2", help="second input file")
    ap.add_argument("out", help="output file")
    ap.add_argument("-r", "--relative", help="interpret file paths as relative to songs dir (if defined via config)", action="store_true")
    args = ap.parse_args()
    file1 = args.file1
    file2 = args.file2
    output = args.out
    if args.relative:
        try:
            songsdir = PurePath(getsongsdir())
        except:
            print("songs dir must be defined when using -r!")
            return
        file1 = songsdir.joinpath(file1)
        file2 = songsdir.joinpath(file2)
        output = songsdir.joinpath(output)
    concat(file1, file2, output)

if __name__ == "__main__":
    main()
