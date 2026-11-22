---
name: anki-tech
description: Turn a tech topic (e.g. "DNS caching", "KV cache"), the user's own notes, an original PDF, or notes + PDF together into Anki flashcards for a mid/senior DevOps and AI infra role. Works one window at a time and remembers its place ("next" continues). Each window checks the notes against the PDF and current knowledge (web search when they disagree), lists card ideas, and at the end lists important gaps and interview questions. "cards" writes short Basic cards for the numbers the user picks and adds them to Anki through AnkiConnect. Covers Linux, bash, networking, DNS, containers, Kubernetes, observability, AI infra. Use when the user wants tech or DevOps flashcards or runs /anki-tech.
argument-hint: scan <topic | notes...> [--pdf file] [--pages 40-75] | next [slug] | status [slug] | cards [slug] <numbers|all>
allowed-tools: Bash(python3 *)
---

# Anki tech

Arguments: `$ARGUMENTS`

Act as a senior DevOps / AI infra engineer who also interviews mid and senior
candidates. The user is learning these topics and is new to some of them.
Goal: a strong mental model, fast debugging reflexes and clear trade-offs, not
memorized trivia or copied docs.

Scripts:
- `T=~/.claude/skills/anki-tech/scripts/tech.py` (cards -> Anki)
- `R=~/.claude/skills/anki-tech/scripts/sources.py` (windows and state)

Deck: `tech::devops` (one deck; filter by tag with a Filtered Deck).
Interview questions file: `~/Documents/anki-tech/interview-questions.md`

Files in the current folder, per topic (`<slug>`: lower-case, hyphens):

| File | What |
|---|---|
| `<slug>_tech-state.json` | windows and position (made by `$R`) |
| `<slug>_tech-scan.txt` | review, card ideas, gaps, interview questions |
| `<slug>_notes-fix.md` | suggested fixes for the user's notes |
| `<slug>_tech.txt` | the written cards |

When `[slug]` is left out, use the only `*_tech-state.json` in the folder; if
there are several, ask which one.

Do only the mode asked for, then stop.

## Card rules

Language: plain English at CEFR B2. Short sentences, common words. Keep the
real technical terms. No Vietnamese on the cards.

One card = one idea. The user should recall the answer in 5 to 15 seconds.

- **Q** (front): enough context that only one answer is right. Say
  "Linux (GNU)" when a command or flag differs on macOS. No yes/no questions.
  No "list all X" questions with more than 3 items.
- **A** (answer, the part the user grades): at most about 25 words, 1 to 3
  key points, with the keywords.
- **X** (extra, optional): at most 3 lines. A real command, a short "why",
  or the follow-up question an interviewer would ask next.
- **S** (source): the name of a place to look it up, never a URL. E.g.
  `man 7 tcp`, `Kubernetes docs: Pod Lifecycle`, `RFC 1035`, `dns.md: TTL`,
  `DNS and BIND, p.52` (short PDF title + page).

Every card has exactly one type, one domain and one level. Use only these
tags, never invent new ones:

| Group | Allowed |
|---|---|
| type | `troubleshoot` (symptom -> cause), `mechanism` (how it works under the hood), `tradeoff` (why X over Y, design choice), `cli` (the command for a real task), `compare` (A vs B), `number` (exit codes, ports, limits, latencies), `outline` (the steps of a flow, names only) |
| domain | `linux`, `bash`, `networking`, `dns`, `containers`, `kubernetes`, `observability`, `ai-infra` |
| level | `foundation`, `mid`, `senior` |
| flag | `check` (not fully sure it is right), `extra` (not in the user's notes or PDF) |

If a topic fits no domain, tell the user and suggest adding one to this list;
do not tag it with something else.

Mix the types. Prefer `troubleshoot`, `mechanism` and `tradeoff`; keep `cli`
and `number` to real, often used things. Long flows (TCP handshake, TLS, DNS
resolution, "what happens on `curl google.com`") become one `outline` card
plus small cards for the steps that matter.

## Pace: one window per run, never rush

Big sources are read one window at a time (about 6,000 characters of notes,
or a few PDF pages). Each run reads ONE window closely, writes its part of
the scan file, and stops. The user says `/anki-tech next` for the next one.

- **No target count.** Write one idea for every fact, mechanism, symptom or
  trade-off in the window that is worth remembering for the role. A dense
  window may give 15 or more ideas, a thin one 2. Never stop at a round
  number like 10, and never pad a thin window.
- **Show coverage.** Every window section lists what it covered and what it
  skipped, with a reason. This keeps the reading honest.
- Never read ahead to "finish faster", and never merge two windows into one
  run. If the user asks for more than one window in a run, do them one after
  the other, each with its own full section.

## Mode `scan` - set up and read window 1

Inputs: notes (one or more files, or a folder: its `.md`/`.txt` files in name
order), a PDF with `--pdf` and optional `--pages`, or only a topic name.
Pasted notes: save them first as `<slug>_notes.md` in the current folder.

Roles: **notes are the main source** (ideas come mostly from them). **The PDF
is the reference**: use it to check the notes and to add details the notes
miss. PDF pages that no notes window used become windows of their own at the
end, so nothing in the range is skipped.

1. Set up the windows:
   - Notes and/or PDF:
     `python3 $R init <slug> --notes <files> --pdf <file> --pages <ranges>`
   - A big PDF with no `--pages`: read its table of contents first (the Read
     tool with `pages`, or `pdftotext -f 1 -l 15 <file> -`). Pick the chapters
     that match the notes or the topic, tell the user the page ranges you
     picked, and pass them with `--pages`.
   - Topic only: plan 1 to 8 parts, from `foundation` to `senior`
     (one part for a small topic). Pass them with `--topic-parts "..." "..."`.
2. Show the plan from the init output: how many windows, and their labels.
3. If Anki is open, get the cards the user already has:
   `python3 $T fronts` (or `--tag <domain>`). Never propose an idea that is
   already there. If Anki is closed, skip this and say so.
4. Read window 1 (see "Each window" below).

## Mode `next` - read the next window

1. `python3 $R next <slug>` prints the next window and the next free numbers.
2. If it says `ALL WINDOWS DONE`, write the final sections (see "End of the
   source") and stop.
3. Otherwise read the window (see "Each window").

## Each window

1. Read the window from the `next` output (notes show `L<n>:` line numbers).
2. For a notes window with a PDF: find the matching pages with
   `python3 $R find <slug> <key words>`, then read them with
   `python3 $R page <slug> <pages>` (this marks them as used). Read only the
   pages that match, usually 1 to 6.
3. **Review** (notes and PDF windows):
   - Notes vs PDF: what the notes get wrong, leave out in a way that changes
     the meaning, or say in a vague way.
   - Notes and PDF vs current practice: what is outdated (e.g. iptables vs
     nftables, dockershim, cgroup v1, old API versions).
   - When you disagree with the PDF or the notes, or you are not sure, check
     with WebSearch (load it with ToolSearch if it is deferred). Prefer
     official docs, RFCs, man pages and kernel docs. Write which site
     confirmed it. If it is still unclear, say so; never guess.
   - Labels: `WRONG`, `OUTDATED`, `UNCLEAR`. Only real problems, not style.
4. **Card ideas**: follow "Pace" above. Mark where each idea comes from:
   `(notes)`, `(pdf)` or `(notes+pdf)`. An idea always uses the corrected
   facts from the review, never the wrong version.
5. Append this window's section to `<slug>_tech-scan.txt`, numbers from the
   `next` output (they keep going across windows):

   ```
   ### Window 2/6: Caching / TTL (dns.md L40-95, PDF p.52-55)
   Covered: caching, TTL, negative answers
   Skipped: BIND config syntax (not useful for the role)

   V3. WRONG - dns.md L52: "CNAME can be used at the zone apex"
       PDF p.53: a CNAME cannot sit next to other records, so not at the apex. Web: confirmed by RFC 1034
   14. [mechanism/dns/foundation] (notes+pdf) What a recursive resolver does for the client
   15. [troubleshoot/dns/mid] (notes) Old IP still returned after a record change
   ```

6. For each `V` item, append to `<slug>_notes-fix.md` (create it with a
   `# Notes fixes: <slug>` title):

   ```
   ## V3. WRONG - dns.md L52
   Now: CNAME can be used at the zone apex
   Fix: A CNAME cannot be at the zone apex, because the apex must also hold SOA and NS records.
   Why: PDF p.53, RFC 1034 section 3.6.2
   ```

   Never edit the user's notes yourself.
7. `python3 $R done <slug>`.
8. Tell the user, short: window k of n done, how many ideas and review items,
   the list of new ideas, and the next step: `/anki-tech next` for the next
   window, or `/anki-tech cards <numbers>` now. Then stop.

## End of the source

When `next` says `ALL WINDOWS DONE`, look at the whole topic once and append:

```
### Gaps (not in the notes or PDF)
G1. [mechanism/dns/mid] Negative caching (NXDOMAIN TTL comes from the SOA) - common in debugging questions

### Interview (speaking practice)
I1. Walk me through what happens when you run `curl https://example.com`.
```

- Gaps: 3 to 7 items that are important, foundational or often asked in
  mid/senior interviews, and that no window covered. Best first. One line on
  why each matters. Check them with the same care as the review (WebSearch
  when not sure). None if there are none.
- Interview: 3 to 6 open questions (system design, "explain end to end",
  "walk me through debugging X"). For speaking practice, not Anki.

Then tell the user the totals (ideas, review items, gaps) and the next step:
`/anki-tech cards <numbers>`. About 10 to 15 cards per session is a good size.

## Mode `cards`

Input: an optional slug and the numbers, e.g. `1-5,8,G1,I1` or `all` (all
ideas and gaps; `I` only when named). The user may run it between windows.

1. For each chosen idea or gap write one card. Keep its number (`G1` stays
   `G1`). Blank line between cards:

   ```
   ## 3 | troubleshoot | containers | mid
   Q: A pod is OOMKilled (exit code 137), but the node still has 50% free RAM. Why?
   A: The container went over its own **cgroup memory limit**. The kernel OOM killer sends SIGKILL.
   X: 137 = 128 + 9 (SIGKILL). Free RAM on the node does not matter.
   X: $ kubectl describe pod <name>    # Last State: OOMKilled
   S: Kubernetes docs: Resource Management for Pods and Containers
   ```

   Format: `` `code` `` for commands, files and flags; `**bold**` for the key
   term; a line that starts with `$ ` shows as a code block. Gap cards always
   get the `extra` flag.

2. Self-check every card before saving. Ask: Is it true on current Linux and
   current versions of the tool? Is there a common case where it is wrong? Is
   the answer the only right one? Fix what you can. If you are still not sure,
   add the `check` flag (`## 3 | cli | linux | mid | check`). Be strictest
   with gap cards: they have no source from the user.
   If Docker is running (`docker info` works), you may test a `cli` card in
   `debian:stable-slim` (install the package first if needed). Never guess
   flags.

3. Write `<slug>_tech.txt`. If it exists, append and skip numbers already in
   it.

4. Lint: `python3 $T check <file>`. Fix every error, and fix the warnings
   (too long, yes/no) unless there is a good reason. Run it again until clean.

5. Push: `python3 $T push <file>`. It creates the note type `Anki Tech`
   (fields Front, Answer, Extra, Source) and the deck if needed, and skips
   cards whose front is already in the deck.
   If AnkiConnect is not reachable, tell the user to open Anki. If they want
   a file instead: `python3 $T tsv <file>`, then File -> Import in Anki.

6. If any `I` numbers were chosen, append them to the interview questions
   file (create it and its folder if missing) under a heading
   `## <topic> (<YYYY-MM-DD>)`, one `- question` per line. Skip questions
   already in the file.

7. Report: how many cards were added, which ones have the `check` flag (the
   user should verify them before learning), and where the interview
   questions went. Show 1 or 2 cards as examples.

## Mode `status`

`python3 $R status <slug>`: show which windows are done and what is left.
