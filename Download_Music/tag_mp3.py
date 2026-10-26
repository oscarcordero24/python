import argparse
from pathlib import Path

from mutagen.id3 import ID3, ID3NoHeaderError, TALB, TPE1


def read_tags(path):
    try:
        return ID3(path)
    except ID3NoHeaderError:
        return ID3()


def first_text(tags, frame):
    return tags[frame].text[0] if frame in tags else ""


def tag_file(path, artist, album, dry_run):
    tags = read_tags(path)
    old_artist, old_album = first_text(tags, "TPE1"), first_text(tags, "TALB")
    has_image = bool(tags.getall("APIC"))

    if not dry_run:
        tags.setall("TPE1", [TPE1(encoding=3, text=artist)])
        tags.setall("TALB", [TALB(encoding=3, text=album)])
        tags.delall("APIC")
        tags.save(path)

    image_note = ", image removed" if has_image else ""
    print(f"{path.name}: artist {old_artist!r} -> {artist!r}, album {old_album!r} -> {album!r}{image_note}")


def main():
    parser = argparse.ArgumentParser(
        description="Set each .mp3's artist and album from its folders (Artist/Album/song.mp3) and remove its cover image."
    )
    parser.add_argument("root", help="Folder that contains the artist folders")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without changing any file")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_dir():
        raise SystemExit(f"Not a folder: {root}")

    files = sorted(root.rglob("*.mp3"))
    if not files:
        raise SystemExit(f"No .mp3 files found in {root}")

    done, skipped = 0, []
    for path in files:
        relative = path.relative_to(root)
        if len(relative.parts) < 3:
            skipped.append(relative)
            continue

        album = path.parent.name.strip()
        artist = path.parent.parent.name.strip()
        tag_file(path, artist, album, args.dry_run)
        done += 1

    verb = "would be updated" if args.dry_run else "updated"
    print(f"\n{done} file(s) {verb}.")
    for relative in skipped:
        print(f"Skipped (not inside Artist/Album folders): {relative}")


if __name__ == "__main__":
    main()
