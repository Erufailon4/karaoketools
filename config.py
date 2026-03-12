#!/bin/python3
"""
View and modify the configuration at $HOME/.config/karaoketools/
"""

from common import getconfigdir, getsongsdir, writetofile
import argparse

def main():
    ap = argparse.ArgumentParser(description="view and modify the configuration at $HOME/.config/karaoketools/")
    ap.add_argument("-m", "--mode", choices=["view", "modify"], help="mode of the command")
    ap.add_argument("-o", "--option", choices=["songsdir"], help="name of the option to view/modify")
    ap.add_argument("-v", "--value", help="new value for the option")
    args = ap.parse_args()
    if not args.mode:
        # by default, list all configuration and exit
        try:
            print(f"songsdir: {getsongsdir()}")
        except:
            print("No songsdir defined")
        return
    match args.mode:
        case "view":
            if args.option and args.option == "songsdir":
                try:
                    print(f"songsdir: {getsongsdir()}")
                except:
                    print("No songsdir defined")
            else:
                print("No or wrong option name given")
        case "modify":
            if args.option and args.value and args.option == "songsdir":
                writetofile(getconfigdir().joinpath("songsdir.txt"), args.value)
            else:
                print("No or wrong option name or value given")

if __name__ == "__main__":
    main()
