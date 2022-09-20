# vgmstream-ext-for-multi-channels

## About
It automates processes of making music files from game files having multi channels.

All music are assumed to have basically two channels, and only multi-channel files have four channels. A multi-channel music is split into 1,2 and 3,4 channels, and then combined in sequence and output as separate files.

## Usage
Place mtc.py and the music files in the same directory as the vgmstream file (test.exe). You need to set the file extension before use.
```
$ mtc.py
```
