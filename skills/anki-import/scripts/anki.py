"""Flashcard text file -> Anki, with IPA and Google Cloud TTS audio.

  python3 anki.py parse <input> [--deck D] [--limit N] [-o cards.json]
      Parse cards, mark the ones already in the deck, write JSON with empty "ipa".
  python3 anki.py push <cards.json> [--deck D]
      Make TTS audio for new cards and add them to Anki through AnkiConnect.
  python3 anki.py phrases [--deck D]
      List the bold chunks already in the deck, one per line.
  python3 anki.py tsv <input> [-o out.txt] [--limit N]
      Old flow: write a TSV file for File -> Import (no IPA, no audio).

Auth for TTS: the active gcloud account billed to GOOGLE_TTS_PROJECT if set,
else GOOGLE_TTS_API_KEY, else gcloud with the default project.
Voice: GOOGLE_TTS_VOICE env var (default en-US-Chirp3-HD-Charon).
"""
import argparse
import base64
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

ANKI_URL = "http://127.0.0.1:8765"
MODEL = "Anki Import (IPA + Audio)"
DEFAULT_DECK = "eng::speaking chunks - new"
VOICE = os.environ.get("GOOGLE_TTS_VOICE", "en-US-Chirp3-HD-Charon")
CACHE_DIR = os.path.expanduser("~/.cache/anki-import/audio")

FRONT_TMPL = '<div class="front">{{Front}}</div>\n<div class="audio">{{Audio}}</div>'
BACK_TMPL = (
    "{{FrontSide}}\n<hr id=answer>\n"
    '<div class="ipa">{{hint:IPA}}</div>\n<div class="back">{{Back}}</div>'
)
CSS = """.card { font-family: -apple-system, system-ui, sans-serif; font-size: 20px;
  text-align: left; color: #222; background: #fff; line-height: 1.5; }
.nightMode.card, .night_mode .card { color: #ddd; background: #1e1e1e; }
.front { font-size: 22px; }
.ipa { margin: 8px 0; color: #777; }
.back { font-size: 18px; }"""


# ---------- parsing ----------

def fmt(line):
    line = line.strip().rstrip(".").rstrip()
    line = html.escape(line, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)


def parse_file(path, limit=None):
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n").strip()
    blocks = [b.splitlines() for b in re.split(r"\n\s*\n", text)]
    if limit:
        blocks = blocks[:limit]
    cards, skipped = [], []
    for lines in blocks:
        # [0] term header, [1] example, [2] definition, [3:] Vietnamese + hook
        if len(lines) < 3:
            skipped.append(lines[0] if lines else "")
            continue
        example = lines[1].strip().rstrip(".").rstrip()
        chunk = header_chunk(lines[0])
        bold = re.findall(r"\*\*(.+?)\*\*", example)
        cards.append({
            "chunk": chunk,
            "front": fmt(lines[1]),
            "back": "<br>".join([fmt(lines[2]), "---"] + [fmt(l) for l in lines[3:]]),
            # IPA target: the bold words, else the header chunk
            "phrase": " ... ".join(bold) or chunk,
            "speech": re.sub(r"\*\*", "", example),
            "ipa": "",
        })
        if not bold:
            print(f"Warning: no **bold** in example of '{chunk}'")
    return cards, skipped


def header_chunk(line):
    # "**20. [deal with (someone)]**" or "1. a big [noun] (a big reader)" -> chunk text
    s = re.sub(r"^\s*\**\s*\d+\.\s*", "", line).strip().strip("*").strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return s


# ---------- AnkiConnect ----------

def anki(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(ANKI_URL, body), timeout=30) as r:
            res = json.load(r)
    except urllib.error.URLError:
        sys.exit("Cannot reach AnkiConnect. Open Anki and make sure the AnkiConnect add-on is installed.")
    if res.get("error"):
        raise RuntimeError(f"AnkiConnect {action}: {res['error']}")
    return res["result"]


def anki_up():
    try:
        anki("version")
        return True
    except SystemExit:
        return False


def note(card, deck, audio=""):
    return {
        "deckName": deck,
        "modelName": MODEL,
        "fields": {"Front": card["front"], "Back": card["back"], "IPA": card["ipa"], "Audio": audio},
        "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        "tags": ["anki-import"],
    }


def ensure_model_and_deck(deck):
    if MODEL not in anki("modelNames"):
        anki("createModel", modelName=MODEL, inOrderFields=["Front", "Back", "IPA", "Audio"],
             css=CSS, isCloze=False,
             cardTemplates=[{"Name": "Card 1", "Front": FRONT_TMPL, "Back": BACK_TMPL}])
        print(f"Created note type: {MODEL}")
    anki("createDeck", deck=deck)


def can_add(cards, deck):
    if MODEL not in anki("modelNames"):
        return [True] * len(cards)
    return anki("canAddNotes", notes=[note(c, deck) for c in cards])


# ---------- Google Cloud TTS ----------

def tts_headers():
    # A set project wins over the key: some keys (e.g. Vertex express "AQ.") are rejected by TTS
    project = os.environ.get("GOOGLE_TTS_PROJECT", "").strip()
    key = os.environ.get("GOOGLE_TTS_API_KEY", "").strip()
    if key and not project:
        return {"x-goog-api-key": key}
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True,
                                        stderr=subprocess.DEVNULL).strip()
        project = project or subprocess.check_output(["gcloud", "config", "get-value", "project"],
                                                     text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("No TTS credentials: set GOOGLE_TTS_API_KEY or log in with gcloud.")
    return {"Authorization": f"Bearer {token}", "x-goog-user-project": project}


def synthesize(text, headers):
    os.makedirs(CACHE_DIR, exist_ok=True)
    name = "anki_tts_" + hashlib.sha1(f"{VOICE}|{text}".encode()).hexdigest()[:16] + ".mp3"
    path = os.path.join(CACHE_DIR, name)
    if os.path.exists(path):
        return name, open(path, "rb").read()
    body = json.dumps({
        "input": {"text": text},
        "voice": {"languageCode": "-".join(VOICE.split("-")[:2]), "name": VOICE},
        "audioConfig": {"audioEncoding": "MP3"},
    }).encode()
    req = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", body,
                                 {"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            audio = base64.b64decode(json.load(r)["audioContent"])
    except urllib.error.HTTPError as e:
        sys.exit(f"Google TTS HTTP {e.code}: {e.read().decode()[:500]}")
    open(path, "wb").write(audio)
    return name, audio


# ---------- commands ----------

def cmd_parse(a):
    cards, skipped = parse_file(a.input, a.limit)
    if anki_up():
        for c, ok in zip(cards, can_add(cards, a.deck)):
            c["exists"] = not ok
    else:
        print("Warning: AnkiConnect not reachable, cannot check for existing cards.")
        for c in cards:
            c["exists"] = False
    out = a.output or os.path.splitext(a.input)[0] + "_cards.json"
    json.dump({"deck": a.deck, "cards": cards}, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    new = sum(not c["exists"] for c in cards)
    print(f"Wrote {out}: {len(cards)} cards, {new} new, {len(cards) - new} already in deck '{a.deck}'")
    for s in skipped:
        print(f"Skipped (fewer than 3 lines): {s}")


def cmd_push(a):
    data = json.load(open(a.cards, encoding="utf-8"))
    deck = a.deck or data["deck"]
    ensure_model_and_deck(deck)
    cards = [c for c, ok in zip(data["cards"], can_add(data["cards"], deck)) if ok]
    if not cards:
        print("Nothing new to add.")
        return
    missing = [c["phrase"] for c in cards if not c["ipa"]]
    if missing:
        print(f"Warning: {len(missing)} cards have no IPA: {', '.join(missing[:5])}")
    headers = tts_headers()
    notes = []
    for i, c in enumerate(cards, 1):
        name, audio = synthesize(c["speech"], headers)
        anki("storeMediaFile", filename=name, data=base64.b64encode(audio).decode())
        notes.append(note(c, deck, f"[sound:{name}]"))
        print(f"  audio {i}/{len(cards)}", end="\r")
    print()
    ids = anki("addNotes", notes=notes)
    added = sum(1 for i in ids if i)
    print(f"Added {added} notes to deck '{deck}' (voice {VOICE})")


def cmd_phrases(a):
    # One known chunk per line: the bold words of each Front in the deck
    ids = anki("findNotes", query=f'"deck:{a.deck}"')
    out = set()
    for n in anki("notesInfo", notes=ids):
        front = n["fields"].get("Front", {}).get("value", "")
        found = re.findall(r"<b>(.+?)</b>", front)
        out.add(" ... ".join(found) if found else re.sub(r"<[^>]+>", "", front))
    print("\n".join(sorted(out, key=str.lower)))


def cmd_tsv(a):
    cards, skipped = parse_file(a.input, a.limit)
    out = a.output or os.path.splitext(a.input)[0] + "_anki.txt"
    q = lambda s: '"' + s.replace('"', '""') + '"'
    with open(out, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n#html:true\n#notetype:Basic\n#columns:Front\tBack\n")
        f.write("\n".join(q(c["front"]) + "\t" + q(c["back"]) for c in cards) + "\n")
    print(f"Wrote {len(cards)} cards to {out}")
    for s in skipped:
        print(f"Skipped (fewer than 3 lines): {s}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("parse")
    s.add_argument("input")
    s.add_argument("--deck", default=DEFAULT_DECK)
    s.add_argument("--limit", type=int)
    s.add_argument("-o", "--output")
    s.set_defaults(fn=cmd_parse)
    s = sub.add_parser("push")
    s.add_argument("cards")
    s.add_argument("--deck")
    s.set_defaults(fn=cmd_push)
    s = sub.add_parser("phrases")
    s.add_argument("--deck", default=DEFAULT_DECK)
    s.set_defaults(fn=cmd_phrases)
    s = sub.add_parser("tsv")
    s.add_argument("input")
    s.add_argument("--limit", type=int)
    s.add_argument("-o", "--output")
    s.set_defaults(fn=cmd_tsv)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
