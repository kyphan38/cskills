---
name: anki-cleanup
description: Clean the current folder of files that the anki skills generated (_raw.txt, _cards.txt, saved transcripts, tsv exports, old leftovers) once their cards are in Anki. Moves them to the macOS Trash and never touches the user's own files. Use when the user asks to clean up Anki files or runs /anki-cleanup.
argument-hint: [folder] [deck name]
allowed-tools: Bash(python3 *)
---

# Anki cleanup

Arguments: `$ARGUMENTS` (folder, default: current folder; deck, default
`eng::speaking chunks - new`).

Script: `S=~/.claude/skills/anki-cleanup/scripts/cleanup.py`

1. Dry run: `python3 $S <folder> --deck "<deck>"`
   If it says it cannot reach AnkiConnect, tell the user to open Anki and stop.
2. Show the user the plan in short: what goes to the Trash and why, and what
   is kept. Ask for a clear yes before moving anything.
3. On yes: `python3 $S <folder> --deck "<deck>" --apply`
4. Report what was moved. Files go to the macOS Trash, so they can be put
   back from Finder until the Trash is emptied.

Only files the skills made are looked at:

| File | Goes when |
|---|---|
| `X_cards.txt` (from /anki-chunks cards) | every card in it is in the deck |
| `X_raw.txt` (from /anki-chunks scan) | its `X_cards.txt` goes |
| `transcript_<date>.txt` (saved by scan from a paste) | its cards file goes |
| `*_anki.txt`, `*_anki_test.txt` (tsv export), `*_cards.json` | always |
| `convert.py`, `sample_tts.mp3`, `anki_import.txt`, `anki_test.txt` | always (old steps) |

Every other file is the user's and is never touched, even if it looks done.
The audio cache in `~/.cache/anki-import/audio` is kept.

If the user asks to remove a file the script keeps, ask first and move it to
`~/.Trash` with `mv`. Never delete files for good.
