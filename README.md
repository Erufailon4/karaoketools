## karaoketools

A collection of tools to help with making karaoke songs in the UltraStar format. (Mostly) compliant with the [unversioned specification](https://github.com/UltraStar-Deluxe/format/blob/main/The%20UltraStar%20File%20Format%20%28Unversioned%29.md). The current tools:

- **config.py:** can be used to view and modify the configuration at `$HOME/.config/karaoketools/`
- **fixfilenames.py:** changes the text file's name (and references to audio/video/image files) to be in the "artist - title" format
- **removehyphens.py:** removes hyphens from the end of each note's text while preserving possible whitespace

Running a tool with the `-h` or `--help` option will show the full syntax and options for each tool.

Please note that this project is still a work in progress, so remember to backup your files.
