---
name: anki-import
description: Add flashcards from a text file (blocks of term header, example sentence, definition, Vietnamese meaning, Logic/Hook) straight into Anki with IPA and Google Cloud TTS audio, through AnkiConnect. Use when the user asks to convert or add flashcards to Anki or runs /anki-import.
argument-hint: <file> [deck name] [test] [tsv]
allowed-tools: Bash(python3 *)
---

# Anki import

Arguments: `$ARGUMENTS`

- First argument: the input file. If missing, use `data.txt` in the current folder.
- A deck name, if given. Default deck: `eng::speaking chunks - new`.
- `test`: only the first 2 cards (add `--limit 2` to the parse step).
- `tsv`: old flow, no IPA and no audio:
  `python3 ~/.claude/skills/anki-import/scripts/anki.py tsv <input>` then tell the user to use File -> Import.

Script: `S=~/.claude/skills/anki-import/scripts/anki.py`

## Input format

Cards are separated by a blank line. Each card has these lines:

1. Term header, e.g. `**20. [deal with (someone/something)]**` or `20. deal with` (not shown on the card)
2. Example sentence -> Front (+ audio)
3. Definition, e.g. `[Phrasal Verb - B1] ...` -> Back
4. More lines (`Nghĩa tiếng Việt: ...`, `Logic/Hook: ...`) -> Back, after `---`

`**text**` becomes bold, the trailing `.` of each line is removed.
If parse warns that an example has no bold, tell the user (the card still
works, IPA then uses the header chunk). Cards files made by /anki-chunks
always have bold.

## Steps

1. Anki must be open with the AnkiConnect add-on (code `2055492159`). If the
   script says it cannot reach AnkiConnect, tell the user and stop.
2. Parse: `python3 $S parse <input> --deck "<deck>" -o <scratchpad>/cards.json`
   It marks cards already in the deck with `"exists": true`.
3. IPA: for every card with `"exists": false`, set `"ipa"` to the General
   American IPA of `"phrase"`, between slashes, with stress marks, e.g.
   `"deal with"` -> `/diːl wɪð/`. Keep placeholders like `(someone)` out.
   Save the JSON (keep all other fields as they are).
4. Push: `python3 $S push <scratchpad>/cards.json`
   It creates the note type `Anki Import (IPA + Audio)` and the deck if
   needed, makes one mp3 per new card with Google Cloud TTS (cached in
   `~/.cache/anki-import/audio`, so re-runs cost nothing), and adds the notes.
   Duplicates in the same deck are skipped.
5. Report how many cards were added and to which deck. Show 1-2 examples of
   phrase + IPA.

## Errors

- `Google TTS HTTP 403 ... has not been used ... or it is disabled`: the Cloud
  Text-to-Speech API is off in that project. Tell the user to enable it.
- `API keys are not supported by this API`: the key is not a Cloud TTS key
  (e.g. a Vertex express key starting with `AQ.`). Use gcloud instead: set
  `GOOGLE_TTS_PROJECT` to a project with the TTS API on
  (the user keeps it in `~/.zshrc`).
- `No TTS credentials`: tell the user to set `GOOGLE_TTS_PROJECT` (gcloud) or
  `GOOGLE_TTS_API_KEY` in `~/.zshrc`. Never ask for a key in chat and never print it.
- Change the voice with `GOOGLE_TTS_VOICE` (default `en-US-Chirp3-HD-Charon`).
