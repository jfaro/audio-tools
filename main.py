import sys
import os
from os.path import join, abspath

import subprocess
from glob import glob

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def get_mp3_files(path):
    paths = glob(f'{path}/*.mp3')
    files = [os.path.basename(p) for p in paths]
    return files


def clean_file(path):
    result = subprocess.run([
        'xattr',
        '-d',
        'com.apple.metadata:kMDItemWhereFroms',
        f'{path}'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Removed where from tag")


# Safely access obj[key][0]
def get_or_default(obj: dict, key: str, default: str) -> str:
    if key in obj:
        value = obj[key]
        if len(value) == 0:
            print(f"Error accessing '{key}'")
            return default
        return value[0]
    return default


def print_row(a, b, c, d):
    print(f"{a:<20}{b:<30}{c:<30}{d:<30}")


def print_file_tags(path):
    file = os.path.basename(path)[:19]
    tags = EasyID3(path)
    artist = get_or_default(tags, "title", "")
    album = get_or_default(tags, 'album', "")
    title = get_or_default(tags, 'title', "")
    print_row(file, artist, album, title)


def edit_file_tags(path):
    mp3 = MP3(path, ID3=EasyID3)

    if 'title' not in mp3:
        value = input("Enter title: ")
        mp3['title'] = value  

    if 'artist' not in mp3:
        value = input("Enter artist: ")
        mp3['artist'] = value 

    if 'album' not in mp3:
        value = input("Enter album: ")
        mp3['album'] = value

    # Commit changes
    mp3.save()


def main():
    args = sys.argv

    if len(args) != 3:
        print(f"Usage: '{args[0]} <clean|view|edit> <AUDIO_PATH>")
        exit(1)

    command = args[1]
    base_dir = abspath(args[2])
    print(f"Using directory: {base_dir}\n")

    names = get_mp3_files(base_dir)
    if len(names) == 0:
        print("No mp3 files found")
        exit(1)

    if command == "clean":
        for name in names:
            path = join(base_dir, name)
            print("Cleaning file:", path)
            clean_file(path)
        exit(0)

    if command == "view":
        print_row("file", "artist", "album", "title")
        for name in names:
            path = join(base_dir, name)
            print_file_tags(path)
        exit(0)

    if command == "edit":
        for name in names:
            path = join(base_dir, name)
            print("Editing file:", path)
            edit_file_tags(path)
        exit(0)

    print("Illegal option:", command)
    exit(1)


if __name__ == "__main__":
    main()