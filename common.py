#!/bin/python3
"""
Common functions and classes for all tools
"""

from enum import Enum
from pathlib import Path

def stringfromfile(filename: str) -> str:
    """
    Return the contents of a text file as a string.

    :raises FileNotFoundError: If the file is not found.
    """
    with open(filename) as inputfile:
        text = inputfile.read()
        return text

def linesfromfile(filename: str) -> list[str]:
    """
    Return the lines of a text file as a list of strings.

    :raises FileNotFoundError: If the file is not found.
    """
    lines = stringfromfile(filename).splitlines()
    return lines

def writetofile(filename: str, data: str) -> None:
    """
    Write string data to a new file.
    """
    with open(filename, "w") as outputfile:
        print(data, file=outputfile)

def getconfigdir() -> Path:
    """
    Return the karaoketools config directory of the current user.
    """
    userhome = Path.home()
    return userhome.joinpath(".config", "karaoketools")

def getsongsdir() -> str:
    """
    Return the songs directory from config.

    :raises FileNotFoundError: If the config file is not found.
    :raises RuntimeError: If the config file is empty or too short.
    """
    configdir = getconfigdir()
    path = stringfromfile(configdir.joinpath("songsdir.txt")).strip()
    if len(path) < 2:
        raise RuntimeError()
    return path

def getmaterialsdir() -> str:
    """
    Return the materials directory from config.

    :raises FileNotFoundError: If the config file is not found.
    :raises RuntimeError: If the config file is empty or too short.
    """
    configdir = getconfigdir()
    path = stringfromfile(configdir.joinpath("materialsdir.txt")).strip()
    if len(path) < 2:
        raise RuntimeError()
    return path

def msinbeats(ms: float, bpm: float) -> float:
    """
    Return the given time in milliseconds converted to beats.
    """
    realbpm = bpm*4
    bpms = realbpm/60000
    return bpms*ms

def beatsinms(beats: float, bpm: float) -> float:
    """
    Return the given beats converted to time in milliseconds.
    """
    realbpm = bpm*4
    mspb = 60000/realbpm
    return mspb*beats

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
        """
        Preparse a file, returning the header lines and body lines as separate lists.

        :raises FileNotFoundError: If the file is not found.
        """
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
        """
        Parse a file, populating the header and events attributes of the parser object.

        :raises FileNotFoundError: If the file is not found.
        """
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
        """
        Set the given header to the given value. If header not found, do nothing.
        """
        if header in self.header:
            self.header[header] = value

    def encode(self) -> list[str]:
        """
        Write the contents of the parser object to a list of lines in US format.
        """
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
        """
        Write the contents of the parser object to a file in US format.
        """
        writetofile(filename, "\n".join(self.encode()))

