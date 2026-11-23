"""Read notes and a reference source one window at a time, and remember where we are.

The reference (--ref) is the full original: a PDF, or a text file (.srt
subtitles, .txt, .md, a saved web page). Text files are cut into "pages"
of about 3,000 characters, so --pages and p.N work the same way.

  python3 sources.py init <slug> [--notes F ...] [--ref F [--pages 40-75,120-130]]
                             [--topic-parts "part 1" "part 2" ...] [--window 6000]
      Plan the windows and write ~/Documents/anki-tech/<slug>/<slug>_tech-state.json.
  python3 sources.py next <slug>
      Print the next window (notes with line numbers, or reference pages) and
      the next free numbers in the scan file. Notes come first, then the pages
      that no notes window looked at, then topic parts.
  python3 sources.py find <slug> WORD ...
      Reference pages in range that contain the words, best first.
  python3 sources.py page <slug> 52-54
      Print reference pages and mark them as used (they get no window of their own).
  python3 sources.py done <slug>
      Mark the current window as done.
  python3 sources.py status <slug>
      Show all windows and what is left.
"""
import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_WINDOW = 6000
# Work files live outside any repo, one folder per topic
WORK_DIR = os.path.expanduser(os.environ.get("ANKI_TECH_DIR", "~/Documents/anki-tech"))


# ---------- pure helpers ----------

def parse_ranges(spec):
    """'40-42,50' -> [40, 41, 42, 50]"""
    pages = []
    for part in filter(None, (p.strip() for p in spec.split(","))):
        a, _, b = part.partition("-")
        pages.extend(range(int(a), int(b or a) + 1))
    return sorted(set(pages))


def compact_ranges(pages):
    """[40, 41, 42, 50] -> '40-42,50'"""
    out, pages = [], sorted(pages)
    i = 0
    while i < len(pages):
        j = i
        while j + 1 < len(pages) and pages[j + 1] == pages[j] + 1:
            j += 1
        out.append(str(pages[i]) if i == j else f"{pages[i]}-{pages[j]}")
        i = j + 1
    return ",".join(out)


def split_notes(lines, window):
    """Split a notes file into windows of whole sections, about `window` chars each.

    Returns [(first_line, last_line, label)] with 1-based line numbers. A new
    window starts only at a markdown heading, unless one section alone is too big.
    """
    sections, start = [], 0
    for i, ln in enumerate(lines):
        if i > start and re.match(r"^#{1,6}\s", ln):
            sections.append((start, i - 1))
            start = i
    if lines:
        sections.append((start, len(lines) - 1))

    # Cut a section that is far too big at blank lines
    parts = []
    for a, b in sections:
        size, cut = 0, a
        for i in range(a, b + 1):
            size += len(lines[i]) + 1
            if size >= window * 1.5 and not lines[i].strip():
                parts.append((cut, i))
                cut, size = i + 1, 0
        if cut <= b:
            parts.append((cut, b))

    windows, cur = [], None
    for a, b in parts:
        size = sum(len(lines[i]) + 1 for i in range(a, b + 1))
        if cur and cur[2] + size <= window:
            cur = (cur[0], b, cur[2] + size)
        else:
            if cur:
                windows.append(cur)
            cur = (a, b, size)
    if cur:
        windows.append(cur)

    def label(a, b):
        heads = [lines[i].lstrip("#").strip() for i in range(a, b + 1) if re.match(r"^#{1,6}\s", lines[i])]
        return " / ".join(heads[:3]) + (" ..." if len(heads) > 3 else "") if heads else lines[a].strip()[:60]

    return [(a + 1, b + 1, label(a, b)) for a, b, _ in windows if any(lines[i].strip() for i in range(a, b + 1))]


def group_pages(pages, sizes, window):
    """Group page numbers into runs of consecutive pages, about `window` chars each."""
    groups, cur, size = [], [], 0
    for p in pages:
        if cur and (p != cur[-1] + 1 or size + sizes.get(p, 0) > window):
            groups.append(cur)
            cur, size = [], 0
        cur.append(p)
        size += sizes.get(p, 0)
    if cur:
        groups.append(cur)
    return groups


def next_numbers(text):
    """Next free numbers in a scan file: ideas, V, G, I."""
    def nxt(pat):
        found = [int(m) for m in re.findall(pat, text, re.M)]
        return max(found) + 1 if found else 1
    return {"idea": nxt(r"^(\d+)\.\s"), "V": nxt(r"^V(\d+)\.\s"), "G": nxt(r"^G(\d+)\.\s"), "I": nxt(r"^I(\d+)\.\s")}


# ---------- reference source (PDF or text) ----------

TEXT_PAGE = 3000  # a text file is cut into "pages" of about this many chars


def clean_srt(text):
    """Keep only the spoken lines of an .srt file."""
    out = []
    for ln in text.splitlines():
        if re.match(r"^\d+$", ln.strip()) or "-->" in ln:
            continue
        if ln.strip() and (not out or out[-1] != ln.strip()):
            out.append(ln.strip())
    return "\n".join(out)


def text_pages(text, size=TEXT_PAGE):
    """Cut text into pages of about `size` chars, at line ends."""
    pages, cur, n = [], [], 0
    for ln in text.splitlines():
        cur.append(ln)
        n += len(ln) + 1
        if n >= size:
            pages.append("\n".join(cur))
            cur, n = [], 0
    if any(l.strip() for l in cur):
        pages.append("\n".join(cur))
    return pages


def is_pdf(path):
    return path.lower().endswith(".pdf")


def read_text_ref(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    return text_pages(clean_srt(text) if path.lower().endswith(".srt") else text)


def ref_pages(path, pages):
    """{page: text} for the given pages. PDF pages are real pages; text pages are chunks."""
    if not pages:
        return {}
    if not is_pdf(path):
        all_pages = read_text_ref(path)
        return {p: all_pages[p - 1] for p in pages if 0 < p <= len(all_pages)}
    try:
        out = subprocess.run(["pdftotext", "-f", str(min(pages)), "-l", str(max(pages)), path, "-"],
                             capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("pdftotext is missing. Run: brew install poppler")
    except subprocess.CalledProcessError as e:
        sys.exit(f"pdftotext failed on {path} p.{min(pages)}-{max(pages)}: {e.stderr.strip()[:300]}")
    texts = out.split("\f")
    want = set(pages)
    return {min(pages) + i: t for i, t in enumerate(texts) if min(pages) + i in want}


def ref_page_count(path):
    if not is_pdf(path):
        return len(read_text_ref(path))
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


# ---------- state ----------

def topic_dir(slug):
    return os.path.join(WORK_DIR, slug)


def state_path(slug):
    return os.path.join(topic_dir(slug), f"{slug}_tech-state.json")


def load(slug):
    try:
        return json.load(open(state_path(slug), encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"No {state_path(slug)}. Run init first.")


def save(st):
    os.makedirs(topic_dir(st["slug"]), exist_ok=True)
    json.dump(st, open(state_path(st["slug"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def current(st):
    """The first window that is not done; reference windows are planned when we get there."""
    for w in st["windows"]:
        if not w["done"]:
            return w
    if st.get("ref") and not st.get("ref_planned"):
        left = [p for p in st["ref"]["pages"] if p not in set(st["ref"]["used"])]
        texts = ref_pages(st["ref"]["file"], left)
        sizes = {p: len(t) for p, t in texts.items()}
        left = [p for p in left if sizes.get(p, 0) > 200]  # skip blank or figure-only pages
        for g in group_pages(left, sizes, st["window"]):
            st["windows"].append({"kind": "ref", "pages": g, "label": f"Ref p.{compact_ranges(g)}", "done": False})
        st["ref_planned"] = True
        save(st)
        return current(st)
    return None


# ---------- commands ----------

def cmd_init(a):
    if os.path.exists(state_path(a.slug)) and not a.force:
        sys.exit(f"{state_path(a.slug)} exists. Use status/next, or --force to start over.")
    st = {"slug": a.slug, "window": a.window, "windows": [], "notes": [], "ref": None, "ref_planned": False}
    for f in [os.path.abspath(x) for x in a.notes or []]:
        lines = open(f, encoding="utf-8").read().splitlines()
        st["notes"].append(f)
        for first, last, label in split_notes(lines, a.window):
            st["windows"].append({"kind": "notes", "file": f, "lines": [first, last], "label": label, "done": False})
    ref = os.path.abspath(a.ref or a.pdf) if (a.ref or a.pdf) else None
    if ref:
        count = ref_page_count(ref)
        if not count:
            sys.exit(f"Cannot read the page count of {ref}.")
        pages = parse_ranges(a.pages) if a.pages else list(range(1, count + 1))
        if pages[-1] > count:
            print(f"Warning: {ref} has {count} pages, pages after {count} are left out.")
            pages = [p for p in pages if p <= count]
        if not pages:
            sys.exit("No reference pages left in that range.")
        st["ref"] = {"file": ref, "pages": pages, "used": []}
    for part in a.topic_parts or []:
        st["windows"].append({"kind": "topic", "label": part, "done": False})
    save(st)
    print(f"Wrote {state_path(a.slug)}")
    cmd_status(a)


def cmd_status(a):
    st = load(a.slug)
    for i, w in enumerate(st["windows"], 1):
        mark = "x" if w["done"] else " "
        where = f"{w['file']}:{w['lines'][0]}-{w['lines'][1]}" if w["kind"] == "notes" else w["kind"]
        print(f"[{mark}] {i}. {where} - {w['label']}")
    if st.get("ref"):
        p = st["ref"]
        left = len(set(p["pages"]) - set(p["used"]))
        planned = "planned above" if st.get("ref_planned") else "become windows after the notes"
        print(f"Ref {p['file']}: pages {compact_ranges(p['pages'])}, {len(p['used'])} used by notes windows, "
              f"{left} left ({planned})")
    done = sum(w["done"] for w in st["windows"])
    print(f"{done}/{len(st['windows'])} windows done")


def cmd_next(a):
    st = load(a.slug)
    w = current(st)
    scan = os.path.join(topic_dir(a.slug), f"{a.slug}_tech-scan.txt")
    nums = next_numbers(open(scan, encoding="utf-8").read()) if os.path.exists(scan) else next_numbers("")
    if not w:
        print("ALL WINDOWS DONE. Write the final Gaps and Interview sections.")
        print(f"Next numbers: G{nums['G']}, I{nums['I']}")
        return
    idx = st["windows"].index(w) + 1
    total = len(st["windows"]) + (0 if st.get("ref_planned") or not st.get("ref") else 1)
    more = "" if st.get("ref_planned") or not st.get("ref") else " (+ reference windows later)"
    print(f"=== Window {idx}/{len(st['windows'])}{more}: {w['label']} ===")
    print(f"Next numbers: {nums['idea']}, V{nums['V']}, G{nums['G']}, I{nums['I']}")
    if w["kind"] == "notes":
        lines = open(w["file"], encoding="utf-8").read().splitlines()
        a_, b_ = w["lines"]
        print(f"Source: {w['file']} lines {a_}-{b_}\n")
        for n in range(a_, b_ + 1):
            print(f"L{n}: {lines[n - 1]}")
    elif w["kind"] == "ref":
        print(f"Source: {st['ref']['file']} (pages not covered by any notes window)\n")
        for p, t in ref_pages(st["ref"]["file"], w["pages"]).items():
            print(f"--- p.{p} ---\n{t.strip()}")
    else:
        print("Source: topic part (no file). Plan this part from what a mid/senior interview covers.")


def cmd_find(a):
    st = load(a.slug)
    if not st.get("ref"):
        sys.exit("No reference source in this state.")
    words = [w.lower() for w in a.words]
    hits = []
    for p, t in ref_pages(st["ref"]["file"], st["ref"]["pages"]).items():
        low = t.lower()
        score = sum(low.count(w) for w in words)
        found = sum(1 for w in words if w in low)
        if score:
            hits.append((found, score, p))
    hits.sort(reverse=True)
    for found, score, p in hits[:15]:
        print(f"p.{p}: {found}/{len(words)} words, {score} hits")
    if not hits:
        print("No page matches.")


def cmd_page(a):
    st = load(a.slug)
    if not st.get("ref"):
        sys.exit("No reference source in this state.")
    pages = [p for p in parse_ranges(a.pages) if p in set(st["ref"]["pages"])]
    if not pages:
        sys.exit(f"Pages out of range ({compact_ranges(st['ref']['pages'])}).")
    for p, t in ref_pages(st["ref"]["file"], pages).items():
        print(f"--- p.{p} ---\n{t.strip()}")
    st["ref"]["used"] = sorted(set(st["ref"]["used"]) | set(pages))
    save(st)


def cmd_done(a):
    st = load(a.slug)
    w = current(st)
    if not w:
        print("All windows are already done.")
        return
    w["done"] = True
    save(st)
    left = sum(not x["done"] for x in st["windows"])
    pdf_left = st.get("ref") and not st.get("ref_planned")
    print(f"Done: {w['label']}. {left} windows left" + (" + reference pages not yet covered" if pdf_left else ""))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init")
    s.add_argument("slug")
    s.add_argument("--notes", nargs="+")
    s.add_argument("--ref", help="full original: PDF, .srt, .txt, .md")
    s.add_argument("--pdf", help="same as --ref")
    s.add_argument("--pages")
    s.add_argument("--topic-parts", nargs="+")
    s.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_init)
    for name, fn in (("next", cmd_next), ("done", cmd_done), ("status", cmd_status)):
        s = sub.add_parser(name)
        s.add_argument("slug")
        s.set_defaults(fn=fn)
    s = sub.add_parser("find")
    s.add_argument("slug")
    s.add_argument("words", nargs="+")
    s.set_defaults(fn=cmd_find)
    s = sub.add_parser("page")
    s.add_argument("slug")
    s.add_argument("pages")
    s.set_defaults(fn=cmd_page)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
