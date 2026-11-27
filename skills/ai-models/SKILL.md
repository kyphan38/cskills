---
name: ai-models
description: Check which Gemini model and thinking level every AI task in the ws/app apps uses, test new or cheaper models side by side on the apps' real prompts (~/ws/app/ai-evals), and recommend per task whether to keep, move down or move up. Use when Google ships a new Gemini model, when prices change, when the user wants to cut AI cost, or runs /ai-models.
argument-hint: [new model ids, e.g. gemini-4-neon gemini-4-carbon]
allowed-tools: Bash(npm run *), Bash(node *), Bash(git *)
---

# AI models check

Arguments: `$ARGUMENTS` (model ids to try; none = only check the current setups).

Repo: `~/ws/app/ai-evals`. Read its `README.md` ("How to decide", "Coverage") first.

## 1. Facts first

- Prices: read https://aistudio.google.com/docs/pricing (Standard paid tier, all dated
  changes, free tier). Update `src/prices.json`. Note models that are deprecated or route
  elsewhere.
- Which models exist for the key: `GET https://generativelanguage.googleapis.com/v1beta/models`
  through a small node script that loads `../fina/.env.local` itself. Never print or read the key.
- Probe each new model once for the thinking levels it accepts (low, medium, high; `minimal`
  is usually rejected).

## 2. Is the inventory current?

`npm run list` shows each task with its current setup. Grep the apps for model ids and
thinking levels (`gemini-[0-9]`, `thinkingLevel`, `thinking:`, cogi `DEFAULTS`, hodi and navi
`GEMINI_MODEL_*`). If a task's `current` differs from the app, or an app has a new AI call
with no task, fix the task file first (README "Add a task"). Tell the user what changed.

## 3. Run

```
npm run eval -- --try <model>:<level>,... [--app ...] [--runs 2]
```

Pick candidates per tier, not every combination:

- Flash tier tasks (lists, parsing, short text): the new cheap model at `low`.
- Strong tier tasks (judge tasks: analysis, coaching, drill scoring): the new models at
  `low` and `medium`, and `default` for models that bill no thinking.

Run in the background when it is over ~2 minutes. Afterwards read `report.md` and,
for judge tasks, `outputs.md`.

## 4. Judge

Follow README "How to decide". For judge tasks, read the outputs side by side yourself
and say in one line per task what is better or worse (accuracy, depth, tone, language).
A failing check on the current setup is either an app bug or a stale task: look before
blaming the model.

## 5. Report to the user (Vietnamese, simple words)

- A table: app, task, current setup, recommendation (keep / move to X:level), why,
  cost per call now and later.
- Total monthly effect only if the hub /costs page or aiUsage data gives call counts.
- Bugs the eval found in the apps.
- Ask before changing any app. Apps differ in how to ship (see the gemini-model memory:
  hodi, legi, navi, noda need a functions deploy; cogi, fina, logi deploy on push).
  After a change, update the task's `current` here and run that app's tasks once more.
