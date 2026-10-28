"""Move files made by the anki skills out of a folder, into the macOS Trash.

  python3 cleanup.py [folder] [--deck D]          dry run: show the plan
  python3 cleanup.py [folder] [--deck D] --apply  move the listed files to ~/.Trash

Only skill-made files are looked at:
  X_cards.txt      goes when every card in it is already in the deck
  X_raw.txt        goes with its X_cards.txt
  transcript_<date>.txt (saved by /anki-chunks scan) goes with its cards too
  *_anki.txt, *_anki_test.txt, *_cards.json, and old leftovers always go
Files the user made (any other name) are never touched.
"""
import argparse
import os
import re
import shutil
import sys
import time

sys.path.insert(0, os.path.expanduser("~/.claude/skills/anki-import/scripts"))
import anki  # noqa: E402

LEFTOVERS = {"convert.py", "sample_tts.mp3", "anki_import.txt", "anki_test.txt"}
ALWAYS_SUFFIXES = ("_anki.txt", "_anki_test.txt", "_cards.json")
SAVED_TRANSCRIPT = re.compile(r"^transcript_\d{4}-\d{2}-\d{2}\.txt$")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("folder", nargs="?", default=".")
    p.add_argument("--deck", default=anki.DEFAULT_DECK)
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()

    folder = os.path.abspath(a.folder)
    names = sorted(f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)))
    trash, keep = {}, {}

    cards_files = [f for f in names if f.endswith("_cards.txt")]
    if cards_files and not anki.anki_up():
        sys.exit("Cannot reach AnkiConnect. Open Anki first, so cleanup can check what is imported.")
    done = set()
    for f in cards_files:
        cards, _ = anki.parse_file(os.path.join(folder, f))
        missing = sum(ok for ok in anki.can_add(cards, a.deck))
        stem = f[: -len("_cards.txt")]
        if missing:
            keep[f] = f"{missing}/{len(cards)} cards not in '{a.deck}' yet"
        else:
            trash[f] = f"all {len(cards)} cards are in '{a.deck}'"
            done.add(stem)

    for f in names:
        if f in trash or f in keep:
            continue
        if f in LEFTOVERS or f.endswith(ALWAYS_SUFFIXES):
            trash[f] = "made by an old step"
        elif f.endswith("_raw.txt"):
            stem = f[: -len("_raw.txt")]
            if stem in done:
                trash[f] = "its cards are all imported"
            else:
                keep[f] = "no fully imported _cards.txt yet"
        elif SAVED_TRANSCRIPT.match(f):
            if f[:-4] in done:
                trash[f] = "saved by scan, its cards are all imported"
            else:
                keep[f] = "saved by scan, cards not fully imported yet"

    print(f"Folder: {folder}")
    print("\nMove to Trash:" if trash else "\nNothing to move to Trash.")
    for f, why in trash.items():
        print(f"  {f}  ({why})")
    if keep:
        print("\nKeep for now:")
        for f, why in keep.items():
            print(f"  {f}  ({why})")
    other = [f for f in names if f not in trash and f not in keep]
    if other:
        print("\nYour files, not touched:", ", ".join(other))

    if not a.apply:
        if trash:
            print("\nDry run. Run again with --apply to move these files.")
        return
    tdir = os.path.expanduser("~/.Trash")
    for f in trash:
        dst = os.path.join(tdir, f)
        if os.path.exists(dst):
            root, ext = os.path.splitext(f)
            dst = os.path.join(tdir, f"{root} {time.strftime('%H.%M.%S')}{ext}")
        shutil.move(os.path.join(folder, f), dst)
    print(f"\nMoved {len(trash)} files to the Trash.")


if __name__ == "__main__":
    main()
