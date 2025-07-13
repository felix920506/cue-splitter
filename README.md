# cue-splitter

## Install and Usage Instructions:

Example Docker Compose:
```yml
services:
  cuesplitter:
    image: ghcr.io/felix920506/cue-splitter:latest
    volumes:
      - ./input:/input
      - ./output:/output
    user: 1000:1000
```

Usage:

1. In the input folder, drop a flac or wav or bin file alongside a cue file with the same name, eg. `something.flac` + `something.cue`. Case sensitive and the extension must be lower case. A jpg or png image of the same name may optionally be added.
2. The program should pick them up automatically. Wait for the program to process the file.
3. The input audio file will be split into individual tracks according to the cue file and saved in the output folder as flac tracks tagged with metadata from the cue file.
4. The input files will be deleted once the processing is complete

Known limitations / issues:
1. The input folder must not be a network share or any other non-local file system
2. Docker on non-Linux platforms may be problematic
3. Cue files not in UTF-8 may cause problems.
4. Cue files not terminated with a trailing new line may cause problems.

## Dev Instructions:

0. Linux ONLY
1. Install python 3.13
2. Install [uv](https://github.com/astral-sh/uv) to install dependencies and manage venv
3. Install other required packages: flac, shntool, cuetools
