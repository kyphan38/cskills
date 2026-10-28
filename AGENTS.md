# Agent instructions (cskills)

cskills holds every Claude Code skill of the owner (`skills/`) and a static
site that lists them (cskills.kyphan38.com). `~/.claude/skills` is a symlink
to `skills/`, so editing a skill edits this repo.

## Skills

- One folder per skill: `SKILL.md` (for Claude), `guide.md` (for the site,
  Vietnamese), plus any `scripts/` or reference files.
- Change a skill → update its `guide.md` in the same change.
- The repo is public: no keys, tokens, project ids or personal data.

### guide.md format

```
---
summary: one short line
family: anki
order: 1
---

## Any heading
Prose, lists, tables.
- `/skill args` - a list item that starts with a command becomes a command row
1. numbered lists become steps

### Example title
(fenced block with lang `input`, then one with lang `output`)
```

Skills in the same `family` are shown as one flow, in `order`.

## Site

Next.js static export, no server. `src/lib/skills.ts` reads `skills/` at
build time. Follow `../DESIGN.md` (gray only, motion rules).

## Git

Format: `<type>(<scope>): <summary>` (Conventional Commits, imperative,
lowercase, no trailing period, <= 72 chars). Commit only. Do not push
unless explicitly asked. Never add `Co-Authored-By:`.

## Writing

No em dash anywhere. Code, comments and UI words in plain English;
`guide.md` and `PLAN-*.md` may be Vietnamese.

# This is NOT the Next.js you know

This version has breaking changes. Read the relevant guide in
`node_modules/next/dist/docs/` before writing code.
