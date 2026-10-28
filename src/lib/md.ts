// A small Markdown reader: only what SKILL.md and guide.md use.
// Blocks stay plain data, so pages can render patterns (commands, steps,
// input/output examples) as their own components.

export type Block =
  | { t: 'h'; depth: number; text: string }
  | { t: 'p'; text: string }
  | { t: 'ul'; items: string[] }
  | { t: 'ol'; items: string[] }
  | { t: 'code'; lang: string; text: string }
  | { t: 'table'; head: string[]; rows: string[][] };

export type Front = Record<string, string>;

export function splitFront(src: string): { front: Front; body: string } {
  const m = src.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!m) return { front: {}, body: src };
  const front: Front = {};
  for (const line of m[1].split('\n')) {
    const i = line.indexOf(':');
    if (i > 0) front[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return { front, body: src.slice(m[0].length) };
}

const FENCE = /^(\s*)(`{3,})(\S*)/;
const HEAD = /^(#{1,6})\s+(.*?)\s*$/;
const UL = /^\s*[-*]\s+(.*)$/;
const OL = /^\s*\d+\.\s+(.*)$/;
const cells = (line: string) =>
  line
    .trim()
    .replace(/^\||\|$/g, '')
    .split('|')
    .map((c) => c.trim());

export function parse(src: string): Block[] {
  const lines = src.replace(/\r\n?/g, '\n').split('\n');
  const out: Block[] = [];
  let para: string[] = [];
  let list: { t: 'ul' | 'ol'; items: string[] } | null = null;

  const flush = () => {
    if (para.length) out.push({ t: 'p', text: para.join(' ') });
    para = [];
    if (list) out.push(list);
    list = null;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const fence = line.match(FENCE);
    if (fence) {
      flush();
      const [, indent, ticks, lang] = fence;
      const body: string[] = [];
      for (i++; i < lines.length && !lines[i].trimStart().startsWith(ticks); i++) {
        body.push(lines[i].startsWith(indent) ? lines[i].slice(indent.length) : lines[i]);
      }
      out.push({ t: 'code', lang, text: body.join('\n') });
      continue;
    }
    if (!line.trim()) {
      flush();
      continue;
    }
    const head = line.match(HEAD);
    if (head) {
      flush();
      out.push({ t: 'h', depth: head[1].length, text: head[2] });
      continue;
    }
    if (line.trimStart().startsWith('|') && /^\s*\|?[\s:-]+\|/.test(lines[i + 1] ?? '')) {
      flush();
      const head = cells(line);
      const rows: string[][] = [];
      for (i += 2; i < lines.length && lines[i].trimStart().startsWith('|'); i++) rows.push(cells(lines[i]));
      i--;
      out.push({ t: 'table', head, rows });
      continue;
    }
    const ul = line.match(UL);
    const ol = ul ? null : line.match(OL);
    if (ul || ol) {
      const t = ul ? 'ul' : 'ol';
      if (para.length || (list && list.t !== t)) flush();
      list ??= { t, items: [] };
      list.items.push((ul ?? ol)![1]);
      continue;
    }
    // An indented line after a list item belongs to that item.
    if (list && /^\s{2,}/.test(line)) {
      list.items[list.items.length - 1] += ' ' + line.trim();
      continue;
    }
    if (list) flush();
    para.push(line.trim());
  }
  flush();
  return out;
}

/** Plain text for search and summaries: no backticks, stars or links. */
export function plain(s: string): string {
  return s
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
}
