import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ViewTransition } from 'react';

import Blocks, { sectionId } from '@/components/Blocks';
import CopyWord from '@/components/CopyWord';
import Disclosure from '@/components/Disclosure';
import EscapeBack from '@/components/EscapeBack';
import Header from '@/components/Header';
import Page from '@/components/Page';
import Toc from '@/components/Toc';
import { plain } from '@/lib/md';
import { familyOf, getSkill, getSkills, REPO } from '@/lib/skills';

export const dynamicParams = false;

export function generateStaticParams() {
  return getSkills().map((s) => ({ name: s.name }));
}

function size(n: number): string {
  return n < 1024 ? `${n} B` : `${(n / 1024).toFixed(1)} KB`;
}

export default async function SkillPage({ params }: PageProps<'/s/[name]'>) {
  const { name } = await params;
  const skill = getSkill(name);
  if (!skill) notFound();
  const family = familyOf(skill);
  const at = family.findIndex((s) => s.name === skill.name);
  const toc = skill.guide
    .filter((b) => b.t === 'h' && b.depth <= 2)
    .map((b, i) => ({ id: sectionId(i + 1), label: plain(b.t === 'h' ? b.text : '') }));

  return (
    <>
      <Header skill={skill.name} />
      <EscapeBack />
      <Page>
        <div className="grid gap-x-16 pt-12 md:grid-cols-[15rem_minmax(0,40rem)] md:pt-16">
          <aside className="md:sticky md:top-10 md:self-start">
            <ViewTransition name={`skill-${skill.name}`} share="morph" default="none">
              <h1 className="inline-block font-mono text-[22px] leading-tight tracking-tight text-ink">{skill.name}</h1>
            </ViewTransition>
            <p className="mt-3 text-[15px] leading-[1.65] text-muted">{skill.summary}</p>

            <div className="mt-6 border border-line-strong px-3 py-2.5">
              <div className="flex items-baseline gap-3">
                <code className="min-w-0 flex-1 truncate font-mono text-[13px] text-ink">
                  <span className="text-faint">$ </span>/{skill.name}
                </code>
                <CopyWord text={`/${skill.name} `} className="shrink-0" />
              </div>
              {skill.hint && <div className="mt-1.5 break-words font-mono text-[11px] leading-relaxed text-faint">{skill.hint}</div>}
            </div>

            {family.length > 1 && (
              <nav aria-label="flow" className="mt-8">
                <div className="mb-2 font-mono text-[11px] tracking-[0.06em] text-faint uppercase">flow</div>
                <ol>
                  {family.map((s, i) => (
                    <li key={s.name} className="relative flex items-center gap-3 py-1">
                      {/* A hairline joins the squares, so the family reads as one pipeline. */}
                      {i < family.length - 1 && <span aria-hidden className="absolute top-[18px] left-[3.5px] h-full w-px bg-line-strong" />}
                      <span
                        aria-hidden
                        className={`relative size-2 shrink-0 border ${i === at ? 'border-ink bg-ink' : 'border-line-strong bg-bg'}`}
                      />
                      {i === at ? (
                        <span className="font-mono text-[12px] text-ink">{s.name}</span>
                      ) : (
                        // Later steps slide in from the right, earlier ones from the left.
                        <Link
                          href={`/s/${s.name}/`}
                          transitionTypes={[i > at ? 'nav-forward' : 'nav-back']}
                          className="font-mono text-[12px] text-faint hover:text-ink"
                        >
                          {s.name}
                        </Link>
                      )}
                    </li>
                  ))}
                </ol>
              </nav>
            )}

            <div className="mt-8 hidden md:block">
              <Toc items={toc} />
            </div>
          </aside>

          <div className="mt-14 min-w-0 md:mt-0">
            <Blocks blocks={skill.guide} />

            <div className="mt-16 border-b border-line">
              <Disclosure label="SKILL.md" meta="what Claude reads">
                <div className="pb-4 text-[14px]">
                  <Blocks blocks={skill.source} compact />
                </div>
              </Disclosure>
              <Disclosure label="files" meta={String(skill.files.length)}>
                <ul className="pb-4 font-mono text-[12.5px]">
                  {skill.files.map((f) => (
                    <li key={f.path} className="flex items-baseline justify-between gap-4 py-1">
                      <a href={`${REPO}/blob/main/skills/${skill.name}/${f.path}`} className="min-w-0 truncate text-muted hover:text-ink">
                        {f.path}
                      </a>
                      <span className="shrink-0 text-faint tabular-nums">{size(f.size)}</span>
                    </li>
                  ))}
                </ul>
              </Disclosure>
            </div>
            <a href={`${REPO}/tree/main/skills/${skill.name}`} className="mt-4 inline-block font-mono text-[12px] text-faint hover:text-ink">
              view on github ↗
            </a>
          </div>
        </div>
      </Page>
    </>
  );
}
