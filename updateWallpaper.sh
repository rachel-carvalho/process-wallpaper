#!/bin/bash

export DISPLAY=:1
top -l3 -s0 -stats pid,command,mem,cpu > top.out
nice python3 generateWallpaper.py
