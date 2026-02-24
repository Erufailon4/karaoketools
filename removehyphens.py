#!/bin/python3
"""
Remove trailing hyphens from karaoke files
"""

import common
import argparse

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
    args = ap.parse_args()
    removehyphens(args.file)

if __name__ == "__main__":
    main()
