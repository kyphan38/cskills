'use client';

import { type ReactNode, useId, useState } from 'react';

// A row that opens a part of the page. The height snaps (DESIGN.md: no
// animated height); the content rises in and the "+" turns into "×".
export default function Disclosure({ label, meta, children }: { label: string; meta?: string; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const id = useId();
  return (
    <section className="border-t border-line">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={id}
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-baseline gap-3 py-3.5 text-left font-mono text-[13px] text-ink transition-colors hover:bg-wash active:bg-wash"
      >
        <span
          aria-hidden
          className={`inline-block w-3 text-center text-[14px] text-faint transition-transform duration-200 ease-[var(--ease-soft)] ${open ? 'rotate-45' : ''}`}
        >
          +
        </span>
        <span>{label}</span>
        {meta && <span className="ml-auto pr-1 text-[12px] text-faint">{meta}</span>}
      </button>
      {open && (
        <div id={id} className="rise pl-6">
          {children}
        </div>
      )}
    </section>
  );
}
