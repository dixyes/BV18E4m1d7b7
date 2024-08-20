#!/bin/sh

# 由于obs以流式保存为mkv，所以需要转一下成一般的mkv

ffmpeg -i streaming.mkv -codec copy copied.mkv

