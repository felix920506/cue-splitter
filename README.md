# cue-splitter

## Install Instructions:

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

## Dev instructions:

0. Linux ONLY
1. Install python 3.13
2. Install [uv](https://github.com/astral-sh/uv) to install dependencies and manage venv
3. Install other required packages: flac, shntool, cuetools
