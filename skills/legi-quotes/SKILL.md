---
name: legi-quotes
description: Turn a book or a talk (PDF, .txt, a folder of video transcripts, or pasted text, English or Vietnamese) into Vietnamese notes ready to paste into legi - quotes, short summaries, story cards, practical rules, a speaker's own words. Works one window of about 3,500 characters at a time and remembers each book (profile, names, position, what is done). Modes - "check" sets up a new book, "next" reads the next window. Use when the user gives a passage, file or book and asks for quotes, notes, key ideas or "câu hay", or runs /legi-quotes.
argument-hint: check <file> | next <book> | <file or pasted text> [pages or chapter] [focus]
allowed-tools: Bash(pbcopy *), Bash(cat *), Bash(wc *), Bash(ls *), Bash(mkdir *)
---

# legi quotes

Arguments: `$ARGUMENTS`

Turn a book into notes the user can paste straight into legi (their quote
app). Keep what is worth remembering, in words that are easy to read again
months later, one random quote at a time.

Library folder: `~/Downloads/books`. Each book has a book file there:
`<slug>.book.md` (slug = short lowercase name, e.g. `mossad`, `quyen-luc-dia-ly`).

## Modes

Pick the mode from the arguments. Do only that mode, then stop.

### `check <file>` - set up a new book

1. Read the start of the book: title page, table of contents, and 2 or 3
   sample pages from the middle. For a PDF use the Read tool with `pages`
   (at most 20 pages per call).
2. Choose a profile (see Profiles below). Read that profile file.
3. Tell the user, in Vietnamese, short:
   - what the book is and how it is built (e.g. "mỗi chương là một chiến dịch"),
   - the profile you picked and why, in one line,
   - whether the profile fits as it is. If the book needs something the
     profile does not cover, say what, and suggest the extra rule,
   - how sections in legi should look (e.g. one `#` per chapter),
   - the window size (default 3,500 characters, about 2 PDF pages),
   - names and terms that will come up often, with the Vietnamese spelling
     you will use.
4. Ask the user to confirm or change. On yes, write the book file (format
   below) and say the next step: `/legi-quotes next <slug>`. Do not write
   notes in this mode.

A folder (e.g. one speaker's video transcripts) is one book: read the start
of 2 or 3 files for the check, and list every file under `## Sources`.

If a book file already exists, show it and ask if the user wants to change it.

### `next <book>` - read the next window

1. Find `~/Downloads/books/<book>.book.md` (match the slug loosely). If there
   is none, run `check` on the source the user gives instead.
2. Read the profile file named in the book file.
3. Read one window from `position`: about `window` characters (PDF: the next
   pages, about 2). A book file with `## Sources` (a folder of transcripts)
   keeps a position per source: continue the first source that is not done. If a story or argument does not end inside the window,
   keep reading until it ends (at most 3 windows). A note must never be cut
   in the middle of a story.
4. Write the notes (rules below), then update the book file: new `position`,
   new names, and one line per note in `Done`.

### `<file or text> [pages or chapter] [focus]` - one part

- A file with a page range or chapter name: read only that part.
- Pasted text: use it. If no book is named, save it as
  `~/Downloads/books/passage_<YYYY-MM-DD>.txt` first (never over an old one).
- Focus words (e.g. "tập trung đoạn người Anh"): only write notes about that
  focus, but in more detail than usual.
- If a book file exists for this source, use it (profile, names, Done) and
  update it after. If not, guess the profile and say which one you used.

Every mode works one window at a time, also for a whole chapter: read about
3,500 characters, write the notes for that window, then read the next one.
Never read a whole chapter first and write after: a close look per window is
the point. A story that runs past a window is finished in the next one before
its card is written. Dedupe across the whole run.

## Reading a PDF

1. Try the Read tool with `pages` (at most 20 pages per call).
2. If it fails (poppler missing), run `pdftotext -f <first> -l <last> <file> -`.
3. If `pdftotext` is missing too, tell the user to run `brew install poppler`
   once, and stop.

Scanned books have OCR errors ("Melr" for Meir, "1" for "I", broken quote
marks). Fix names from context and never copy the errors. Write the fixes
you made often into the book file's notes, so they stay the same.

## Profiles

One profile per book, in `profiles/` next to this file:

- `geopolitics.md` - geography, politics, history of countries, economics.
- `story.md` - stories: spy missions, wars, history told as events,
  biographies. Uses story cards that may be long.
- `practical.md` - skills: communication, work, habits, negotiation.
- `talk.md` - spoken sources: livestreams, podcasts, interviews, Q&A clips
  (auto subtitles). The speaker's own words come first.

If no profile fits well, use the closest one and say what is missing.

## Rules for every note (all profiles)

**Stand alone (most important).** legi shows one random note a day, months
later, with no chapter around it.

- Name the subject: "Iran", "Mossad", "Isser Harel", never "nước này",
  "ông", "họ", "tổ chức này" without a name.
- Anchor a place the first time: "sông Shatt al-Arab, ở biên giới phía tây
  Iran giáp Iraq".
- Give a person their role: "Isser Harel, giám đốc Mossad".
- Give a year when the book gives one.
- Check: read the note alone. If you ask "who?", "where?" or "when?", fix it.

**Language and style.**

- Always Vietnamese, also for English books. Keep proper names in their usual
  form (Eichmann, Mossad, Shin Bet). Use the Vietnamese names in the book file.
- Plain words, like telling a friend. Short sentences, about 20 words.
  No literary or academic words when a common one works: write "đánh bại",
  not "bách chiến bách thắng"; "chia nhỏ", not "xé lẻ".
- A hard term gets a short meaning in brackets the first time:
  "quốc hữu hóa (chuyển thành của nhà nước)".
- Never use the em dash. Use ` - `, a comma, or two sentences.
- No bold: never write `**...**` (the owner's style).
- No period at the end of a paragraph (the owner's style). Periods between
  sentences inside a paragraph stay. A paragraph may end with `:` or `?`.
- A note with several parts (a list, a story card) puts each part in its
  own paragraph, with one blank line between paragraphs.

**Book and outside knowledge.**

- Facts must match the book: names, numbers, dates.
- You may add a little outside knowledge when it makes a note clearer or
  gives needed context (who someone is, what a term means, how two people are
  related, what happened next). Keep it short and well known.
- Write outside facts normally, with no label: never `Theo sách`, `Ngoài sách`,
  `Ngoài video` or similar. Context words fit inside a sentence: "vùng
  Lưỡng Hà (Iraq và Syria ngày nay)". A longer outside fact gets its own
  paragraph. If you are not sure a fact is true, leave it out.
- Never add your own comment, irony or conclusion ("Người sau này làm giám
  đốc Mossad từng bị loại..."). If a sentence is neither in the book nor a
  known fact, delete it before you show the notes. Do not leave it for the
  user to delete.

**What to skip.** Filler, repeats, small talk of the author, ideas already
in the book file's `Done` list (unless the new part adds something - then
write one better note and say which old one it replaces).

**How many.** Quality over count. A rough guide: 3 to 6 notes per 3,500
characters for facts and ideas; a good story is one card however long.
A window that is mostly in `Done` gives few new notes, and that is right:
say how much of the window was already done.

**Read what was asked.** "The first 3,500 characters of chapter 1" starts at
the chapter's first word, even if that part is in `Done`. Report the real
range you read (pages and roughly which part), not the range you meant to.

## Output file

Never overwrite a file. Name the output by what it covers:
`~/Downloads/books/<slug>_legi_<part>.txt`, where `<part>` is the page range
(`p28-36`), the chapter (`ch3`) or the date (`2026-10-28`) for pasted text.
If that name is taken, add `-2`, `-3`, ... (`mossad_legi_p28-36-2.txt`).
Check with `ls` before writing. The same goes for saved pasted text
(`passage_<date>.txt`, then `passage_<date>-2.txt`). Format for legi's paste:

- Every note starts with its own line `--- p52`: three dashes, a space and
  the page where the note's story or idea starts. A source with no page
  numbers (pasted text without page marks) uses `---` alone.
- Inside a note, one blank line between paragraphs. No numbers, no bullets,
  no labels like `[tóm tắt]`.
- `# Title` starts a new section, `## Title` a section inside it. A heading
  goes on its own line before the `---` of the section's first note. The
  user pastes while the right parent section is open in legi, so headings
  nest under it. Use the section names from the book file, so the same
  section is not made twice.

Example:

```
--- p13
Meir Dagan trong các cuộc chiến của Israel:

Chiến tranh Yom Kippur (1973): Dagan là một trong những người Israel đầu tiên vượt kênh đào Suez (Ai Cập), trong một đơn vị trinh sát

Chiến tranh Lebanon (1982): Dagan dẫn lữ đoàn thiết giáp của mình tiến vào Beirut. Ông nói: "Ngay cả trước khi lữ đoàn xe tăng của tôi vào Beirut, tôi đã biết rõ thành phố này"

--- p14
Meir Dagan, giám đốc Mossad (2002-2011), ...
```

## Book file format

```
# <Book title>
source: <path to the PDF or txt>
profile: story
legi book: <title as in legi>
position: page 34   (or: char 12000 for a txt)
window: 3500

## Sections
- # Bắt Eichmann (1960)

## Names
- Isser Harel: giám đốc Mossad (1952-1963)

## Done
- p12-15 | Eichmann | story card: bắt Eichmann ở Buenos Aires
```

Keep `Done` lines short: page, topic, a few words. It is for dedupe, not a copy.

## After writing

1. Copy the output file to the clipboard: `cat <file> | pbcopy`.
2. Show the user, in Vietnamese:
   - the file path, the pages or characters read, and the note count,
   - which legi section to open before pasting,
   - the notes themselves, each tagged with its form from the profile
     (`[nguyên văn]`, `[rút gọn]`, `[tóm tắt]`, `[story]`, `[nhân vật]`,
     `[câu hay]`, `[nguyên tắc]`, `[quy tắc]`, `[câu mẫu]`,
     `[bức tranh lớn]`), plus `+ngoài sách` when it has outside facts
     (only in chat, never in the file).
     A quote with added context is `[câu hay]`, not `[nguyên văn]`,
   - one line: "Đã copy, mở đúng section trong legi rồi dán vào ô nhập."
3. Stop. Do not open legi or change anything else.
