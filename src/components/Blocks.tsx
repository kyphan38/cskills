import Command from '@/components/Command';
import Example from '@/components/Example';
import Inline from '@/components/Inline';
import type { Block } from '@/lib/md';

const COMMAND = /^`([^`]+)`\s*(?:-\s*)?(.*)$/;

/** Anchor of the n-th section heading (1-based); the table of contents uses the same ids. */
export const sectionId = (n: number) => `s-${n}`;

// Renders parsed Markdown. Three patterns get their own look:
// a list of `command` - text items, a numbered list (steps), and an
// h3 followed by an `input` and an `output` code block (an example).
export default function Blocks({ blocks, compact = false }: { blocks: Block[]; compact?: boolean }) {
  const out: React.ReactNode[] = [];
  let section = 0;
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i];
    const next = blocks[i + 1];
    const after = blocks[i + 2];

    if (b.t === 'h' && b.depth === 3 && next?.t === 'code' && next.lang === 'input' && after?.t === 'code' && after.lang === 'output') {
      out.push(<Example key={i} title={b.text} input={next.text} output={after.text} />);
      i += 2;
      continue;
    }

    switch (b.t) {
      case 'h':
        out.push(
          b.depth <= 2 && !compact ? (
            <h2
              key={i}
              id={sectionId(++section)}
              className="mt-16 mb-5 flex scroll-mt-8 items-baseline gap-3 border-t border-line pt-4 font-mono text-[12px] tracking-[0.06em] text-faint uppercase first:mt-0"
            >
              <span className="tabular-nums">{String(section).padStart(2, '0')}</span>
              <span className="text-ink">
                <Inline text={b.text} />
              </span>
            </h2>
          ) : b.depth <= 2 ? (
            <h2 key={i} className="mt-6 mb-3 font-mono text-[12px] text-faint">
              <Inline text={b.text} />
            </h2>
          ) : (
            <h3 key={i} className="mt-6 mb-2 text-[14px] font-medium text-ink">
              <Inline text={b.text} />
            </h3>
          ),
        );
        break;
      case 'p':
        out.push(
          <p key={i} className={`my-3 ${compact ? 'text-[14px]' : 'text-[16px]'} leading-[1.75] text-ink`}>
            <Inline text={b.text} />
          </p>,
        );
        break;
      case 'ul':
        if (!compact && b.items.every((it) => COMMAND.test(it) && it.startsWith('`/'))) {
          out.push(
            <ul key={i} className="divide-y divide-line">
              {b.items.map((it, j) => {
                const [, cmd, text] = it.match(COMMAND)!;
                return <Command key={j} cmd={cmd} text={text} />;
              })}
            </ul>,
          );
        } else {
          out.push(
            <ul key={i} className="my-3 space-y-1.5">
              {b.items.map((it, j) => (
                <li key={j} className={`relative pl-4 ${compact ? 'text-[14px]' : 'text-[15px]'} leading-[1.7] text-ink`}>
                  <span aria-hidden className="absolute left-0 text-faint">
                    ·
                  </span>
                  <Inline text={it} />
                </li>
              ))}
            </ul>,
          );
        }
        break;
      case 'ol':
        out.push(
          <ol key={i} className="my-3">
            {b.items.map((it, j) => (
              <li key={j} className="relative flex gap-4 pb-4 last:pb-0">
                {/* A hairline joins the step numbers, so the list reads as one path. */}
                {j < b.items.length - 1 && <span aria-hidden className="absolute top-6 bottom-0 left-[9px] w-px bg-line" />}
                <span className="w-5 shrink-0 text-center font-mono text-[12px] leading-[1.7rem] text-faint tabular-nums">{j + 1}</span>
                <span className={`${compact ? 'text-[14px]' : 'text-[15px]'} leading-[1.7] text-ink`}>
                  <Inline text={it} />
                </span>
              </li>
            ))}
          </ol>,
        );
        break;
      case 'code':
        out.push(
          <pre
            key={i}
            className="my-3 overflow-x-auto rounded-[3px] bg-sunk px-4 py-3 font-mono text-[12.5px] leading-[1.65] text-muted"
          >
            {b.text}
          </pre>,
        );
        break;
      case 'table':
        out.push(
          <div key={i} className="my-3 overflow-x-auto">
            <table className="w-full border-collapse text-left text-[13px]">
              <thead>
                <tr>
                  {b.head.map((c, j) => (
                    <th key={j} className="border-b border-line-strong py-1.5 pr-4 font-medium text-faint">
                      <Inline text={c} />
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {b.rows.map((r, j) => (
                  <tr key={j}>
                    {r.map((c, k) => (
                      <td key={k} className="border-b border-line py-1.5 pr-4 align-top leading-relaxed text-ink">
                        <Inline text={c} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>,
        );
        break;
    }
  }
  return <>{out}</>;
}
