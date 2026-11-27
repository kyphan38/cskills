---
name: upkeep
description: Act on the monthly upkeep reports for the ws/app apps (~/ws/app/upkeep): workspace rule findings, library updates, AI price tables and the logged vs billed AI cost gap. Runs the checks first when the reports are old. Use when the macOS "upkeep: reports ready" notification shows, when the user asks to update libraries, check costs or tidy the workspace rules, or runs /upkeep.
argument-hint: [lint | deps | costs] (default: all three)
allowed-tools: Bash(npm run *), Bash(node *), Bash(git *), Bash(npm *)
---

# Upkeep

Arguments: `$ARGUMENTS` (one of lint, deps, costs; none = all).

Repo: `~/ws/app/upkeep`. Read its `README.md` first.

## 1. Fresh reports

Reports live in `reports/<day>/{lint,deps,costs}.md`. If the newest is older than a
week, run `npm run lint`, `npm run deps`, `npm run costs` first (deps takes a few
minutes). `costs` needs `gcloud auth login`; if it says so, ask the user to log in.

## 2. Plan, then ask

Read the reports and write one short plan in Vietnamese (simple words), grouped by app:

- **lint**: em dash, underline, co-author: fix them. Emoji: only real emoji in UI text
  (arrows and check marks may be fine, ask). Files over 500 lines: list only; split one
  only when the user picks it. AI calls without cost logging: fix. AI calls not named
  in ai-evals: add a task (upkeep/ai-evals README "Add a task") or say why the tier is
  already covered.
- **deps**: patch and minor per app folder. Major ones: one line each with what
  changes (read the release notes) and a yes/no for the user. Respect the HOLD list in
  `checks/deps.ts`; never bump `firebase-admin` in cogi/web without its sign-in probe.
- **costs**: wrong prices: update every copy of `ai-cost.ts` / `aiCost.ts` (they must
  stay the same file; functions apps have a test for it). A gap under 70% logged:
  look for Gemini calls that skip logAiCost and for models missing from the table.

Ask before starting. The user may pick only some lines.

## 3. Do it, one app at a time

1. Check the branch and `git status`; stage explicit paths only (other sessions work here).
2. Make the change. For deps: `npm update` (or `npm install pkg@x` for one package),
   then the app's tests, typecheck, lint and build.
3. Commit per app with the app's commit format. Push and deploy only if the user said
   so; follow each app's AGENTS.md (several are "commit only").
4. A failing test after an update: revert that package and note it. Do not force it.

## 4. Close

Run the checks again and report what changed: a short table per app (done, skipped,
waiting for a decision). If a held-back package is now safe, update the HOLD note.
