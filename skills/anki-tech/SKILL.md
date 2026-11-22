---
name: anki-tech
description: Turn a tech topic (e.g. "DNS caching", "KV cache") or the user's own docs into Anki flashcards for a mid/senior DevOps and AI infra role, in two steps - "scan" lists card ideas and open interview questions, "cards" writes short Basic cards for the numbers the user picks, self-checks them and adds them to Anki through AnkiConnect. Covers Linux, bash, networking, DNS, containers, Kubernetes, observability, AI infra. Use when the user wants tech or DevOps flashcards or runs /anki-tech.
argument-hint: scan <topic | file | folder> | cards [scan file] <numbers|all>
allowed-tools: Bash(python3 *)
---

# Anki tech

Arguments: `$ARGUMENTS`

Act as a senior DevOps / AI infra engineer who also interviews mid and senior
candidates. The user is learning these topics and is new to some of them.
Goal: a strong mental model, fast debugging reflexes and clear trade-offs, not
memorized trivia or copied docs.

Script: `S=~/.claude/skills/anki-tech/scripts/tech.py`
Deck: `tech::devops` (one deck; filter by tag with a Filtered Deck).
Interview questions file: `~/Documents/anki-tech/interview-questions.md`

Two modes. Do only the one asked for, then stop.

## Card rules (both modes)

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
  `man 7 tcp`, `man 1 ss`, `Kubernetes docs: Pod Lifecycle`, `RFC 1035`. In
  docs mode: the file name and heading.

Every card has exactly one type, one domain and one level. Use only these
tags, never invent new ones:

| Group | Allowed |
|---|---|
| type | `troubleshoot` (symptom -> cause), `mechanism` (how it works under the hood), `tradeoff` (why X over Y, design choice), `cli` (the command for a real task), `compare` (A vs B), `number` (exit codes, ports, limits, latencies), `outline` (the steps of a flow, names only) |
| domain | `linux`, `bash`, `networking`, `dns`, `containers`, `kubernetes`, `observability`, `ai-infra` |
| level | `foundation`, `mid`, `senior` |
| flag | `check` (not fully sure it is right), `extra` (docs mode: not in the user's docs) |

If a topic fits no domain, tell the user and suggest adding one to this list;
do not tag it with something else.

Mix the types. Prefer `troubleshoot`, `mechanism` and `tradeoff`; keep `cli`
and `number` to real, often used things. Long flows (TCP handshake, TLS, DNS
resolution, "what happens on `curl google.com`") become one `outline` card
plus small cards for the steps that matter.

## Mode `scan`

Input: a topic name, a file, a folder of files, or pasted text.

- Docs (file, folder or paste): read all of it. Ideas come from the docs. You
  may add up to 3 ideas that are not in them; mark those `extra`.
- Topic only: plan from what a mid/senior interview would cover, from
  `foundation` up.

1. If Anki is open, get what the user already has:
   `python3 $S fronts` (or `--tag <domain>`). Leave out ideas that are already
   there. If Anki is closed, skip this and say so.
2. List 15 to 25 card ideas. Order them from `foundation` to `senior`.
3. List 3 to 6 open interview questions on the same topic (system design,
   "explain end to end", "walk me through debugging X"). These are for
   speaking practice, not for Anki.
4. Write `<slug>_tech-scan.txt` in the current folder (slug from the topic or
   file name, lower-case, hyphens):

   ```
   1. [mechanism/dns/foundation] What a recursive resolver does for the client
   2. [troubleshoot/dns/mid] Old IP still returned after a record change
   ...

   Interview (speaking practice)
   I1. Walk me through what happens when you run `curl https://example.com`.
   ```

5. Show the path, the count and the list. Tell the user the next step:
   `/anki-tech cards 1-5,8,I1` (or `all`). About 10 to 15 cards per session is
   a good size. Then stop.

## Mode `cards`

Input: an optional scan file (default: the newest `*_tech-scan.txt` in the
current folder) and the numbers to use, e.g. `1-5,8,I1` or `all`.

1. For each chosen idea write one card. Keep its number. Blank line between
   cards:

   ```
   ## 3 | troubleshoot | containers | mid
   Q: A pod is OOMKilled (exit code 137), but the node still has 50% free RAM. Why?
   A: The container went over its own **cgroup memory limit**. The kernel OOM killer sends SIGKILL.
   X: 137 = 128 + 9 (SIGKILL). Free RAM on the node does not matter.
   X: $ kubectl describe pod <name>    # Last State: OOMKilled
   S: Kubernetes docs: Resource Management for Pods and Containers
   ```

   Format: `` `code` `` for commands, files and flags; `**bold**` for the key
   term; a line that starts with `$ ` shows as a code block.

2. Self-check every card before saving. Ask: Is it true on current Linux and
   current versions of the tool? Is there a common case where it is wrong? Is
   the answer the only right one? Fix what you can. If you are still not sure,
   add the `check` flag to the header (`## 3 | cli | linux | mid | check`).
   If Docker is running (`docker info` works), you may test a `cli` card in
   `debian:stable-slim` (install the package first if needed). Never guess
   flags.

3. Write `<slug>_tech.txt` in the current folder. If it exists, append and
   skip numbers already in it.

4. Lint: `python3 $S check <file>`. Fix every error, and fix the warnings
   (too long, yes/no) unless there is a good reason. Run it again until clean.

5. Push: `python3 $S push <file>`. It creates the note type `Anki Tech`
   (fields Front, Answer, Extra, Source) and the deck if needed, and skips
   cards whose front is already in the deck.
   If AnkiConnect is not reachable, tell the user to open Anki. If they want
   a file instead: `python3 $S tsv <file>`, then File -> Import in Anki.

6. If any `I` numbers were chosen, append them to the interview questions
   file (create it and its folder if missing) under a heading
   `## <topic> (<YYYY-MM-DD>)`, one `- question` per line. Skip questions
   already in the file.

7. Report: how many cards were added, which ones have the `check` flag (the
   user should verify them before learning), and where the interview
   questions went. Show 1 or 2 cards as examples.
