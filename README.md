## karaoketools

A collection of tools to help with making karaoke songs in the UltraStar format. (Mostly) compliant with the [unversioned specification](https://github.com/UltraStar-Deluxe/format/blob/main/The%20UltraStar%20File%20Format%20%28Unversioned%29.md). The current tools:

- **concat.py:** "concatenates" two files with the same BPM, copying notes from the one with a longer gap to the one with a shorter gap, adjusting note start times to match the shorter gap
- **config.py:** can be used to view and modify the configuration at `$HOME/.config/karaoketools/`
- **info.py:** prints information about the song to stdout, with the option to convert beat values to time in seconds
- **fixfilenames.py:** changes the text file's name (and references to audio/video/image files) to be in the "artist - title" format
- **removehyphens.py:** removes hyphens from the end of each note's text while preserving possible whitespace

Running a tool with the `-h` or `--help` option will show the full syntax and options for each tool.

This is just something that I've made for my own use and may not live up to any standard, even my own. If you for some reason decide to use it, remember to backup your files.
