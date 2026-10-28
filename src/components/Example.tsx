'use client';

import { useEffect, useRef, useState } from 'react';

import { reducedMotion } from '@/lib/motion';

// An input/output pair. The output writes itself word by word the first
// time it scrolls into view, so you see the skill "work". Fast on purpose:
// the whole output takes at most ~1.2s. "replay" runs it again.
const MAX_MS = 1200;

export default function Example({ title, input, output }: { title: string; input: string; output: string }) {
  const words = output.split(/(\s+)/);
  const [shown, setShown] = useState(words.length);
  const [running, setRunning] = useState(false);
  const box = useRef<HTMLDivElement>(null);
  const done = useRef(false);
  const timer = useRef<number | null>(null);

  const run = () => {
    if (reducedMotion()) return;
    if (timer.current) cancelAnimationFrame(timer.current);
    const start = performance.now();
    const total = Math.min(MAX_MS, words.length * 18);
    setRunning(true);
    setShown(0);
    const tick = (now: number) => {
      const n = Math.ceil(((now - start) / total) * words.length);
      setShown(Math.min(n, words.length));
      if (n < words.length) timer.current = requestAnimationFrame(tick);
      else setRunning(false);
    };
    timer.current = requestAnimationFrame(tick);
  };

  useEffect(() => {
    const el = box.current;
    if (!el || reducedMotion()) return;
    const io = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !done.current) {
          done.current = true;
          run();
          io.disconnect();
        }
      },
      { threshold: 0.4 },
    );
    io.observe(el);
    return () => {
      io.disconnect();
      if (timer.current) cancelAnimationFrame(timer.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div ref={box} className="my-6">
      <div className="flex items-baseline justify-between gap-4">
        <h3 className="text-[14px] font-medium text-ink">{title}</h3>
        <button
          type="button"
          onClick={run}
          className="font-mono text-[12px] text-faint transition-transform duration-150 hover:text-ink active:scale-[0.97]"
        >
          replay
        </button>
      </div>
      <div className="mt-3 border border-line-strong bg-surface">
        <div className="border-b border-dashed border-line-strong bg-bg px-4 py-3">
          <div className="mb-2 font-mono text-[10.5px] tracking-[0.08em] text-faint uppercase">input</div>
          {/* Book text is hard-wrapped in guide.md: join its lines, keep blank lines. */}
          <pre className="whitespace-pre-wrap break-words font-mono text-[12.5px] leading-[1.7] text-muted">
            {input.replace(/([^\n])\n(?!\n)/g, '$1 ')}
          </pre>
        </div>
        <div className="px-4 py-3">
          <div className="mb-2 font-mono text-[10.5px] tracking-[0.08em] text-faint uppercase">output</div>
          {/* The full text is laid out from the start (invisible tail), so the box never grows while typing. */}
          <p className="relative whitespace-pre-wrap break-words text-[14.5px] leading-[1.75] text-ink" aria-label={output}>
            <span aria-hidden>{words.slice(0, shown).join('')}</span>
            {/* A still caret: DESIGN.md allows no blinking. */}
            {running && <span aria-hidden className="ml-px inline-block h-[1.05em] w-px translate-y-[0.18em] bg-ink" />}
            <span aria-hidden className="opacity-0">
              {words.slice(shown).join('')}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
