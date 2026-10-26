import argparse
from pathlib import Path

from mutagen.id3 import ID3, ID3NoHeaderError, TALB, TPE1


def find_mp3s(target):
    path = Path(target).expanduser()
    if path.is_dir():
        return sorted(path.glob("*.mp3"))
    return [path]


def read_tags(path):
    try:
        tags = ID3(path)
    except ID3NoHeaderError:
        return "", ""
    artist = tags["TPE1"].text[0] if "TPE1" in tags else ""
    album = tags["TALB"].text[0] if "TALB" in tags else ""
    return artist, album


def write_tags(path, artist=None, album=None):
    try:
        tags = ID3(path)
    except ID3NoHeaderError:
        tags = ID3()

    if artist is not None:
        tags.setall("TPE1", [TPE1(encoding=3, text=artist)])
    if album is not None:
        tags.setall("TALB", [TALB(encoding=3, text=album)])
    tags.save(path)


def main():
    parser = argparse.ArgumentParser(description="Set the artist and/or album of an .mp3 file, or of every .mp3 in a folder.")
    parser.add_argument("target", help="An .mp3 file, or a folder of .mp3 files")
    parser.add_argument("--artist", help="New artist (author) name")
    parser.add_argument("--album", help="New album name")
    args = parser.parse_args()

    files = find_mp3s(args.target)
    if not files:
        raise SystemExit(f"No .mp3 files found in {args.target}")

    for path in files:
        if not path.is_file():
            raise SystemExit(f"Not found: {path}")

    for path in files:
        old_artist, old_album = read_tags(path)
        if args.artist is None and args.album is None:
            print(f"{path.name}: artist={old_artist!r} album={old_album!r}")
            continue

        write_tags(path, args.artist, args.album)
        new_artist, new_album = read_tags(path)
        print(f"{path.name}: artist {old_artist!r} -> {new_artist!r}, album {old_album!r} -> {new_album!r}")


if __name__ == "__main__":
    main()
