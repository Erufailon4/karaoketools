#!/bin/python3
"""
Common functions and classes for all tools
"""

from enum import Enum
from pathlib import Path

def stringfromfile(filename: str) -> str:
    with open(filename) as inputfile:
        text = inputfile.read()
        return text

def linesfromfile(filename: str) -> list[str]:
    lines = stringfromfile(filename).splitlines()
    return lines

def writetofile(filename: str, data: str) -> None:
    with open(filename, "w") as outputfile:
        print(data, file=outputfile)

def getconfigdir() -> Path:
    userhome = Path.home()
    return userhome.joinpath(".config", "karaoketools")

def getsongsdir() -> str:
    configdir = getconfigdir()
    path = stringfromfile(configdir.joinpath("songsdir.txt")).strip()
    if len(path) < 2:
        raise RuntimeError()
    return path

class USFEventType(Enum):
    NONE = "NONE"
    NORMAL = ":"
    GOLDEN = "*"
    RAP = "R"
    RAPGOLDEN = "G"
    FREESTYLE = "F"
    ENDOFPHRASE = "-"

class USFEvent:
    def __init__(self, line: str):
        self.type = USFEventType.NONE
        self.start = 0
        self.duration = 0
        self.pitch = 0
        self.text = ""
        lineparts = line.split(maxsplit=4)
        if len(lineparts) < 2:
            raise SyntaxError
        try:
            self.type = USFEventType(lineparts[0])
        except ValueError:
            pass
        self.start = int(lineparts[1])
        if len(lineparts) > 2:
            self.duration = int(lineparts[2])
            self.pitch = int(lineparts[3])
            self.text = lineparts[4]
    
    def __str__(self):
        if self.type == USFEventType.ENDOFPHRASE:
            outputline = f"{self.type.value} {self.start}"
        else:
            outputline = f"{self.type.value} {self.start} {self.duration} {self.pitch} {self.text}"
        return outputline

class USFParser:
    TAGS = {
        "#BPM": "bpm", "#MP3": "mp3", "#TITLE": "title", "#ARTIST": "artist",
        "#COVER": "cover", "#BACKGROUND": "background", "#VIDEO": "video",
        "#GAP": "gap", "#VIDEOGAP": "videogap", "#START": "start", "#END": "end",
        "#PREVIEWSTART": "previewstart", "#MEDLEYSTARTBEAT": "medleystartbeat", 
        "#MEDLEYENDBEAT": "medleyendbeat", "#YEAR": "year", "#GENRE": "genre",
        "#LANGUAGE": "language", "#EDITION": "edition", "#P1": "p1", "#P2": "p2",
        "#DUETSINGERP1": "p1", "#DUETSINGERP2": "p2", "#CREATOR": "creator"
    }
    def __init__(self):
        self.header = {}
        self.events = []
    
    def __str__(self):
        try:
            text = f"{self.header['title']} by {self.header['artist']}\n{len(self.events)} events"
        except:
            text = "Not parsed"
        return text
    
    def preparsefile(self, filename: str) -> dict[str, list]:
        lines = linesfromfile(filename)
        headerlines = []
        bodylines = []
        for line in lines:
            if line.startswith('#'):
                lineparts = line.split(':')
                if len(lineparts) > 1:
                    headerlines.append({"key": lineparts[0], "value": lineparts[1]})
            elif not line.isspace():
                bodylines.append(line)
        return {"header": headerlines, "body": bodylines}
    
    def parsefile(self, filename: str) -> None:
        preparsed = self.preparsefile(filename)
        for headerline in preparsed["header"]:
            if headerline["key"] in USFParser.TAGS:
                self.header.update({USFParser.TAGS[headerline["key"]]: headerline["value"].strip()})
        for bodyline in preparsed["body"]:
            match bodyline[0]:
                case ':' | '*' | 'R' | 'G' | 'F' | '-':
                    self.events.append(USFEvent(bodyline))
                case 'E':
                    break
    
    def modifyheader(self, header: str, value: str) -> None:
        if header in self.header:
            self.header[header] = value

    def encode(self) -> list[str]:
        outputlines = []
        for header in self.header.keys():
            tag = ""
            for x in USFParser.TAGS.items():
                if header == x[1]:
                    tag = x[0]
                    break
            if tag != "":
                outputlines.append(f"{tag}:{self.header[header]}")
        for event in self.events:
            if event.type != USFEventType.NONE:
                outputlines.append(str(event))
        outputlines.append("E")
        return outputlines
    
    def encodetofile(self, filename: str) -> None:
        writetofile(filename, "\n".join(self.encode()))

