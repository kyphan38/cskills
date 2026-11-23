"""Tech flashcard text file -> Anki through AnkiConnect.

  python3 tech.py check <cards.txt> [--deck D]
      Parse and lint the cards, show which ones are already in their deck.
  python3 tech.py push <cards.txt> [--deck D]
      Add the new cards to Anki (note type "Anki Tech"). Each card goes to
      arca::<domain>, unless --deck puts them all in one deck.
  python3 tech.py fronts [--deck D]
      List the front of every card under a deck (default: arca, all note
      types, so cards made by arca's /cards count too), one per line.
  python3 tech.py tsv <cards.txt> [-o out.txt]
      Fallback when Anki is closed: TSV file for File -> Import.

Card format (blank line between cards):

  ## 3 | troubleshoot | containers | mid
  Q: A pod is OOMKilled (exit 137) but the node has free RAM. Why?
  A: It went over its own `cgroup` memory limit, so the kernel sent SIGKILL.
  X: 137 = 128 + 9 (SIGKILL).
  S: Kubernetes docs: Resource Management for Pods and Containers

Header: number | type | domain | level, then optional flags (check, extra).
"""
import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request

ANKI_URL = "http://127.0.0.1:8765"
MODEL = "Anki Tech"
PARENT_DECK = "arca"  # one parent deck: review "arca" to review everything

DOMAINS = {"linux", "bash", "networking", "dns", "containers", "kubernetes", "observability", "ai-infra",
           "aws", "security"}
TYPES = {"troubleshoot", "mechanism", "tradeoff", "cli", "compare", "number", "outline"}
LEVELS = {"foundation", "mid", "senior"}
FLAGS = {"check", "extra"}

MAX_ANSWER_WORDS = 30
MAX_EXTRA_LINES = 3
YES_NO = re.compile(r"^(is|are|does|do|can|should|will|was|were|has|have)\b", re.I)

FRONT_TMPL = '<div class="q">{{Front}}</div>'
BACK_TMPL = (
    '{{FrontSide}}\n<hr id=answer>\n<div class="a">{{Answer}}</div>\n'
    '{{#Extra}}<div class="x">{{Extra}}</div>{{/Extra}}\n'
    '{{#Source}}<div class="s">{{Source}}</div>{{/Source}}'
)
CSS = """.card { font-family: -apple-system, system-ui, sans-serif; font-size: 20px;
  text-align: left; color: #141414; background: #fff; line-height: 1.5; }
.nightMode.card, .night_mode .card { color: #e6e6e6; background: #141414; }
.q { font-size: 21px; }
.a { font-size: 20px; }
.x { margin-top: 14px; font-size: 16px; color: #666; }
.s { margin-top: 14px; font-size: 13px; color: #999; }
.nightMode .x, .night_mode .x { color: #a0a0a0; }
.nightMode .s, .night_mode .s { color: #777; }
code, pre { font-family: ui-monospace, Menlo, monospace; font-size: 0.9em;
  background: rgba(127,127,127,0.14); border-radius: 4px; }
code { padding: 1px 4px; }
pre { padding: 8px 10px; white-space: pre-wrap; margin: 6px 0; }
pre code { background: none; padding: 0; }"""


# ---------- parsing ----------

def inline(s):
    # Escape HTML first, then turn `code` and **bold** into tags
    parts = re.split(r"(`[^`]+`)", s)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1], quote=False) + "</code>")
        else:
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(p, quote=False)))
    return "".join(out)


def render(lines):
    # Lines starting with "$ " are shown as a code block
    out, code = [], []
    for ln in lines + [None]:
        if ln is not None and ln.startswith("$ "):
            code.append(html.escape(ln, quote=False))
            continue
        if code:
            out.append("<pre><code>" + "\n".join(code) + "</code></pre>")
            code = []
        if ln is not None:
            out.append(inline(ln))
    return "<br>".join(out).replace("</pre><br>", "</pre>").replace("<br><pre>", "<pre>")


def parse_file(path):
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    blocks = re.split(r"\n(?=## )", "\n" + text)
    cards, errors = [], []
    for b in blocks:
        b = b.strip()
        if not b.startswith("## "):
            continue
        lines = [l.rstrip() for l in b.splitlines()]
        head = [h.strip().lower() for h in lines[0][3:].split("|")]
        num = head[0] if head else "?"
        f = {"Q": [], "A": [], "X": [], "S": []}
        key = None
        for ln in lines[1:]:
            m = re.match(r"^([QAXS]):\s?(.*)$", ln)
            if m:
                key = m.group(1)
                f[key].append(m.group(2))
            elif ln.strip() and key:
                f[key].append(ln.strip())
        card = {"num": num, "head": head, "raw": f, "problems": []}
        if len(head) < 4:
            errors.append(f"#{num}: header needs 'N | type | domain | level'")
            continue
        typ, dom, lvl, flags = head[1], head[2], head[3], head[4:]
        if typ not in TYPES:
            errors.append(f"#{num}: unknown type '{typ}'")
        if dom not in DOMAINS:
            errors.append(f"#{num}: unknown domain '{dom}'")
        if lvl not in LEVELS:
            errors.append(f"#{num}: unknown level '{lvl}'")
        for fl in flags:
            if fl not in FLAGS:
                errors.append(f"#{num}: unknown flag '{fl}'")
        if not f["Q"] or not f["A"]:
            errors.append(f"#{num}: needs Q: and A:")
            continue
        q = " ".join(f["Q"])
        if YES_NO.match(q):
            card["problems"].append("yes/no question")
        words = len(" ".join(f["A"]).split())
        if words > MAX_ANSWER_WORDS:
            card["problems"].append(f"answer has {words} words (max {MAX_ANSWER_WORDS})")
        if len(f["X"]) > MAX_EXTRA_LINES:
            card["problems"].append(f"extra has {len(f['X'])} lines (max {MAX_EXTRA_LINES})")
        card["fields"] = {
            "Front": render(f["Q"]),
            "Answer": render(f["A"]),
            "Extra": render(f["X"]),
            "Source": inline(" ".join(f["S"])),
        }
        card["tags"] = [dom, typ, lvl] + [fl for fl in flags if fl in FLAGS]
        card["domain"] = dom
        cards.append(card)
    return cards, errors


def load(path):
    cards, errors = parse_file(path)
    for e in errors:
        print("Error " + e)
    if errors:
        sys.exit(f"{len(errors)} errors, fix the file first.")
    return cards


# ---------- AnkiConnect ----------

def anki(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(ANKI_URL, body), timeout=30) as r:
            res = json.load(r)
    except urllib.error.URLError:
        raise ConnectionError("Cannot reach AnkiConnect. Open Anki with the AnkiConnect add-on.")
    if res.get("error"):
        raise RuntimeError(f"AnkiConnect {action}: {res['error']}")
    return res["result"]


def deck_of(card, override=None):
    return override or f"{PARENT_DECK}::{card['domain']}"


def note(card, deck=None):
    return {
        "deckName": deck_of(card, deck),
        "modelName": MODEL,
        "fields": card["fields"],
        "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        "tags": card["tags"],
    }


def can_add(cards, deck=None):
    if MODEL not in anki("modelNames"):
        return [True] * len(cards)
    return anki("canAddNotes", notes=[note(c, deck) for c in cards])


# ---------- commands ----------

def cmd_check(a):
    cards = load(a.cards)
    try:
        ok = can_add(cards, a.deck)
    except ConnectionError as e:
        print(f"Warning: {e} Cannot check for existing cards.")
        ok = [True] * len(cards)
    flagged = 0
    for c, new in zip(cards, ok):
        notes = list(c["problems"])
        if not new:
            notes.append("already in deck")
        if "check" in c["tags"]:
            notes.append("flag: check")
        if notes:
            flagged += 1
            print(f"#{c['num']}: " + "; ".join(notes))
    print(f"{len(cards)} cards, {sum(ok)} new, {flagged} with notes")


def cmd_push(a):
    cards = load(a.cards)
    try:
        if MODEL not in anki("modelNames"):
            anki("createModel", modelName=MODEL, inOrderFields=["Front", "Answer", "Extra", "Source"],
                 css=CSS, isCloze=False,
                 cardTemplates=[{"Name": "Card 1", "Front": FRONT_TMPL, "Back": BACK_TMPL}])
            print(f"Created note type: {MODEL}")
        for d in sorted({deck_of(c, a.deck) for c in cards}):
            anki("createDeck", deck=d)
        new = [c for c, ok in zip(cards, can_add(cards, a.deck)) if ok]
        if not new:
            print("Nothing new to add.")
            return
        ids = anki("addNotes", notes=[note(c, a.deck) for c in new])
    except ConnectionError as e:
        sys.exit(str(e))
    added = sum(1 for i in ids if i)
    decks = ", ".join(sorted({deck_of(c, a.deck) for c in new}))
    print(f"Added {added} notes to {decks}; {len(cards) - len(new)} already there")
    checks = [c["num"] for c in new if "check" in c["tags"]]
    if checks:
        print(f"Tagged 'check' (verify before learning): #{', #'.join(checks)}")


def cmd_fronts(a):
    # Any note type: arca's /cards uses Basic, this skill uses Anki Tech
    try:
        ids = anki("findNotes", query=f'"deck:{a.deck}"')
        infos = anki("notesInfo", notes=ids)
        first_cards = [n["cards"][0] for n in infos if n.get("cards")]
        decks = {c["cardId"]: c["deckName"] for c in anki("cardsInfo", cards=first_cards)}
    except ConnectionError as e:
        sys.exit(str(e))
    for n in infos:
        first = min(n["fields"].values(), key=lambda f: f["order"])["value"]
        text = html.unescape(re.sub(r"<[^>]+>", "", first.replace("<br>", " ")))
        deck = decks.get(n["cards"][0], a.deck) if n.get("cards") else a.deck
        print(f"[{deck}] {text}")


def cmd_tsv(a):
    cards = load(a.cards)
    out = a.output or re.sub(r"\.txt$", "", a.cards) + "_anki.txt"
    q = lambda s: '"' + s.replace('"', '""') + '"'
    with open(out, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n#html:true\n#notetype:Basic\n#deck column:4\n#columns:Front\tBack\tTags\tDeck\n")
        for c in cards:
            fl = c["fields"]
            back = fl["Answer"]
            if fl["Extra"]:
                back += "<br><br>" + fl["Extra"]
            if fl["Source"]:
                back += "<br><br><small>" + fl["Source"] + "</small>"
            f.write(q(fl["Front"]) + "\t" + q(back) + "\t" + " ".join(c["tags"]) + "\t" + deck_of(c) + "\n")
    print(f"Wrote {len(cards)} cards to {out} (note type Basic, no Extra/Source fields)")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("check", cmd_check), ("push", cmd_push)):
        s = sub.add_parser(name)
        s.add_argument("cards")
        s.add_argument("--deck", help="put every card in this deck instead of arca::<domain>")
        s.set_defaults(fn=fn)
    s = sub.add_parser("fronts")
    s.add_argument("--deck", default=PARENT_DECK)
    s.set_defaults(fn=cmd_fronts)
    s = sub.add_parser("tsv")
    s.add_argument("cards")
    s.add_argument("-o", "--output")
    s.set_defaults(fn=cmd_tsv)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
