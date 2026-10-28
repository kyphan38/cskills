'use client';

import CopyWord from '@/components/CopyWord';
import Inline from '@/components/Inline';

// One command of a skill: the command in mono, what it does below.
// "copy" waits for the pointer; on touch it stays visible but faint.
export default function Command({ cmd, text }: { cmd: string; text: string }) {
  return (
    <li className="group flex items-baseline gap-4 py-2.5">
      <div className="min-w-0 flex-1">
        <code className="block break-words font-mono text-[13.5px] text-ink">
          <span aria-hidden className="text-faint">$ </span>
          {cmd}
        </code>
        {text && (
          <p className="mt-1 text-[14px] leading-relaxed text-muted">
            <Inline text={text} />
          </p>
        )}
      </div>
      <CopyWord
        text={cmd}
        className="shrink-0 opacity-0 transition-opacity group-hover:opacity-100 group-focus-within:opacity-100 [@media(hover:none)]:opacity-100"
      />
    </li>
  );
}
