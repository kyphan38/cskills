// Reads skills/ at build time. Only server code imports this file.

import fs from 'node:fs';
import path from 'node:path';

import { type Block, parse, plain, splitFront } from '@/lib/md';

const ROOT = path.join(process.cwd(), 'skills');
export const REPO = 'https://github.com/kyphan38/cskills';

export type SkillFile = { path: string; size: number };

export type Skill = {
  name: string;
  /** Short line from guide.md, else the start of the SKILL.md description. */
  summary: string;
  description: string;
  hint: string;
  family: string;
  order: number;
  guide: Block[];
  source: Block[];
  files: SkillFile[];
};

function walk(dir: string, base = ''): SkillFile[] {
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((e) => !e.name.startsWith('.') && e.name !== '__pycache__')
    .sort((a, b) => a.name.localeCompare(b.name))
    .flatMap((e) => {
      const rel = base ? `${base}/${e.name}` : e.name;
      const full = path.join(dir, e.name);
      return e.isDirectory() ? walk(full, rel) : [{ path: rel, size: fs.statSync(full).size }];
    });
}

function read(name: string): Skill {
  const dir = path.join(ROOT, name);
  const skill = splitFront(fs.readFileSync(path.join(dir, 'SKILL.md'), 'utf8'));
  const guidePath = path.join(dir, 'guide.md');
  const guide = fs.existsSync(guidePath) ? splitFront(fs.readFileSync(guidePath, 'utf8')) : { front: {}, body: '' };
  const description = skill.front.description ?? '';
  return {
    name: skill.front.name ?? name,
    summary: guide.front.summary ?? plain(description.split('. ')[0]),
    description,
    hint: skill.front['argument-hint'] ?? '',
    family: guide.front.family ?? name.split('-')[0],
    order: Number(guide.front.order ?? 99),
    guide: parse(guide.body),
    source: parse(skill.body),
    files: walk(dir),
  };
}

let cache: Skill[] | null = null;

export function getSkills(): Skill[] {
  cache ??= fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((e) => e.isDirectory() && fs.existsSync(path.join(ROOT, e.name, 'SKILL.md')))
    .map((e) => read(e.name))
    .sort((a, b) => a.family.localeCompare(b.family) || a.order - b.order || a.name.localeCompare(b.name));
  return cache;
}

export function getSkill(name: string): Skill | undefined {
  return getSkills().find((s) => s.name === name);
}

/** The other skills of the same family, in order (the flow). */
export function familyOf(skill: Skill): Skill[] {
  return getSkills().filter((s) => s.family === skill.family);
}
