#!/bin/python3
"""
Common functions and classes for all tools
"""

def stringfromfile(filename):
    with open(filename) as inputfile:
        text = inputfile.read()
        return text

def linesfromfile(filename):
    lines = stringfromfile(filename).splitlines()
    return lines

def writetofile(filename,data):
    with open(filename, "w") as outputfile:
        print(data, file=outputfile)

class USFEvent:
    def __init__(self, line):
        self.type = "NONE"
        self.start = 0
        self.duration = 0
        self.pitch = 0
        self.text = ""
        lineparts = line.strip().split()
        if len(lineparts) < 2:
            raise SyntaxError
        match lineparts[0]:
            case ':':
                self.type = "normal"
            case '*':
                self.type = "golden"
            case 'R':
                self.type = "rap"
            case 'G':
                self.type = "rapgolden"
            case 'F':
                self.type = "freestyle"
            case '-':
                self.type = "endofphrase"
        self.start = int(lineparts[1])
        if len(lineparts) > 2:
            self.duration = int(lineparts[2])
            self.pitch = int(lineparts[3])
            self.text = lineparts[4]

class USFParser:
    def __init__(self):
        self.header = {}
        self.events = []
    def __str__(self):
        try:
            text = f"{self.header['title']} by {self.header['artist']}\n{len(self.events)} events"
        except:
            text = "Not parsed"
        return text
    def preparsefile(self, filename):
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
    def parsefile(self, filename):
        preparsed = self.preparsefile(filename)
        for headerline in preparsed["header"]:
            match headerline["key"]:
                case "#BPM":
                    self.header.update({"bpm": headerline["value"].strip()})
                case "#MP3":
                    self.header.update({"mp3": headerline["value"].strip()})
                case "#TITLE":
                    self.header.update({"title": headerline["value"].strip()})
                case "#ARTIST":
                    self.header.update({"artist": headerline["value"].strip()})
        for bodyline in preparsed["body"]:
            match bodyline[0]:
                case ':' | '*' | 'R' | 'G' | 'F' | '-':
                    self.events.append(USFEvent(bodyline))
                case 'E':
                    break

