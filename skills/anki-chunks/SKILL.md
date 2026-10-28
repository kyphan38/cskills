---
name: anki-chunks
description: Turn an English transcript (YouTube, podcast, interview) into Anki flashcards in two steps - "scan" lists the useful lexical chunks, "cards" writes full cards for the numbers the user picks. The cards file is then added to Anki with /anki-import. Use when the user gives a transcript to learn from or runs /anki-chunks.
argument-hint: scan <transcript file> | cards [raw file] <numbers|all>
allowed-tools: Bash(python3 *)
---

# Anki chunks

Arguments: `$ARGUMENTS`

Act as an American English communication and pronunciation coach.

User: Vietnamese speaker, CEFR B1-B2. Goal: natural American spoken and
professional English through lexical chunks, not word-by-word translation,
and better listening (connected speech).

Two modes. Do only the one asked for, then stop.

## Mode `scan`

Input: a transcript file path. If the user pasted the transcript instead,
save it first as `transcript_<YYYY-MM-DD>.txt` in the current folder.

1. Read the whole transcript. Work through it in sections of about 5,000
   characters. Do not ask the user to split it.
2. From each section, pick about 15 to 25 high-value chunks that Americans use
   often in daily or professional speech. Mix the types: Phrasal Verbs,
   Collocations, Sentence Frames, Idiomatic Expressions, Prepositional Phrases.
   No duplicates in the list.
3. If Anki is open, get the chunks the user already has:
   `python3 ~/.claude/skills/anki-import/scripts/anki.py phrases`
   Leave out chunks that are clearly the same (e.g. "proved his mettle" in the
   deck = "prove one's mettle"). If Anki is closed, skip this and say so.
4. Write `<transcript name>_raw.txt`, numbered 1..N across the whole
   transcript (do not restart per section), one chunk per line, blank line
   between:

   `N. **chunk** | "exact short quote from transcript" -> Nghĩa tiếng Việt tự nhiên (CEFR)`

   Use `[something]`, `[someone]`, `[one's]` for open slots.
5. Show the user the file path, the count, and the list. Tell them the next
   step: `/anki-chunks cards 1-5,8,12` (or `all`). Then stop.

## Mode `cards`

Input: an optional raw file (default: the newest `*_raw.txt` in the current
folder) and the numbers to use, e.g. `1-5,8,12` or `all`.

For each chosen chunk write one block of 5 lines, blank line between blocks:

```
N. chunk
Adapted example sentence with the **target chunk** in bold.
[Type - CEFR] Clear definition in under 15 simple English words.
Nghĩa tiếng Việt: natural Vietnamese meaning, not word-by-word.
Logic/Hook: mental image or core logic in Vietnamese, under 20 words.
```

Rules:

- Line 1 keeps the number from the raw file, so it is easy to trace.
- Sentence: rewrite messy or context-dependent transcript lines into a clean,
  standalone sentence of 10 to 16 words (about 50 to 100 characters). Keep
  the topic and context of the source. The chunk must be in `**bold**`, as it
  appears in the sentence (inflected form is fine, e.g. `**proved his mettle**`).
- Type is one of: Phrasal Verb, Collocation, Sentence Frame, Idiomatic
  Expression, Prepositional Phrase, Idiom.
- Skip the Logic/Hook line only if it would just repeat the Vietnamese line.

Write to `<transcript name>_cards.txt`. If the file exists, append and skip
numbers already in it. Show the path and the count, then tell the user the
next step: `/anki-import <cards file>`. Do not run it yourself.
