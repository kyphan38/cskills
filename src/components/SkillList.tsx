'use client';

import Link from 'next/link';
import { useEffect, useLayoutEffect, useMemo, useRef, useState, ViewTransition } from 'react';

import { EASE_SOFT, reducedMotion } from '@/lib/motion';

export type ListItem = { name: string; summary: string; family: string; text: string };

// The home list. Type to filter ("/" jumps to the box), arrow keys move,
// Enter opens. One marker slides between rows instead of each row
// lighting up, so the eye follows a single thing. Rows that stay after a
// filter glide to their new place (FLIP); new ones rise in.
export default function SkillList({ items }: { items: ListItem[] }) {
  const [query, setQuery] = useState('');
  const [active, setActive] = useState(0);
  const [keyboard, setKeyboard] = useState(false);
  const input = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const rows = useRef(new Map<string, HTMLAnchorElement>());
  const lastRects = useRef(new Map<string, DOMRect>());
  const changed = useRef(false);

  const shown = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q ? items.filter((it) => it.text.includes(q)) : items;
  }, [items, query]);

  const order = useMemo(() => shown.map((it) => it.name), [shown]);
  const current = order[Math.min(active, order.length - 1)];

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === '/' && document.activeElement !== input.current) {
        e.preventDefault();
        input.current?.focus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  // FLIP after a filter: only when the user typed, never on first paint.
  useLayoutEffect(() => {
    const now = new Map<string, DOMRect>();
    rows.current.forEach((el, name) => now.set(name, el.getBoundingClientRect()));
    if (changed.current && !reducedMotion()) {
      now.forEach((rect, name) => {
        const el = rows.current.get(name);
        const before = lastRects.current.get(name);
        if (!el) return;
        if (!before) {
          el.animate([{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], {
            duration: 220,
            easing: EASE_SOFT,
          });
        } else if (Math.abs(before.top - rect.top) > 0.5) {
          el.animate([{ transform: `translateY(${before.top - rect.top}px)` }, { transform: 'none' }], {
            duration: 240,
            easing: EASE_SOFT,
          });
        }
      });
    }
    changed.current = false;
    lastRects.current = now;
  }, [order]);

  // The highlight follows the active row with a transform.
  const [mark, setMark] = useState<{ y: number; h: number } | null>(null);
  useLayoutEffect(() => {
    const el = current ? rows.current.get(current) : undefined;
    const box = listRef.current;
    if (!el || !box) return setMark(null);
    const a = el.getBoundingClientRect();
    const b = box.getBoundingClientRect();
    setMark({ y: a.top - b.top, h: a.height });
  }, [current, order]);

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      setKeyboard(true);
      const d = e.key === 'ArrowDown' ? 1 : -1;
      setActive((i) => Math.max(0, Math.min(order.length - 1, i + d)));
    } else if (e.key === 'Enter' && current) {
      rows.current.get(current)?.click();
    } else if (e.key === 'Escape') {
      changed.current = true;
      setQuery('');
    }
  };

  return (
    <div onKeyDown={onKeyDown}>
      <label className="flex items-baseline gap-3 border border-line-strong px-3 py-2.5 font-mono transition-colors focus-within:border-ink">
        <span aria-hidden className="text-[14px] text-ink">
          $
        </span>
        <span aria-hidden className="text-[14px] text-faint">
          find
        </span>
        <input
          ref={input}
          value={query}
          onChange={(e) => {
            changed.current = true;
            setQuery(e.target.value);
            setActive(0);
          }}
          placeholder="a skill, press /"
          aria-label="find a skill"
          className="min-w-0 flex-1 bg-transparent text-[16px] text-ink outline-none placeholder:text-faint md:text-[14px]"
          spellCheck={false}
          autoComplete="off"
        />
        <span className="text-[12px] text-faint tabular-nums">
          {shown.length}/{items.length}
        </span>
      </label>

      <div ref={listRef} className="relative mt-8 border-b border-line" onPointerMove={() => setKeyboard(false)}>
        {/* One marker for the whole index: a 2px bar that slides to the active row. */}
        {mark && (
          <div
            aria-hidden
            className={`pointer-events-none absolute top-0 left-0 w-[2px] bg-ink transition-[transform,opacity] duration-200 ease-[var(--ease-soft)] ${keyboard ? 'opacity-100' : 'opacity-0'}`}
            style={{ transform: `translateY(${mark.y}px)`, height: mark.h }}
          />
        )}
        {shown.map((it) => (
          <Link
            key={it.name}
            href={`/s/${it.name}/`}
            transitionTypes={['nav-forward']}
            ref={(el) => {
              if (el) rows.current.set(it.name, el);
              else rows.current.delete(it.name);
            }}
            onPointerEnter={() => setActive(order.indexOf(it.name))}
            onFocus={() => setActive(order.indexOf(it.name))}
            className="group grid grid-cols-[2.5rem_1fr_auto] items-baseline gap-x-3 border-t border-line py-4 pl-3 transition-colors hover:bg-wash active:bg-wash md:grid-cols-[3rem_14rem_1fr_6rem_1.5rem]"
          >
            <span className="font-mono text-[12px] text-faint tabular-nums">{String(items.indexOf(it) + 1).padStart(2, '0')}</span>
            <ViewTransition name={`skill-${it.name}`} share="morph" default="none">
              <span className="font-mono text-[15px] text-ink">{it.name}</span>
            </ViewTransition>
            <span className="col-start-2 col-end-4 mt-1 text-[14px] leading-relaxed text-muted md:col-start-auto md:col-end-auto md:mt-0">
              {it.summary}
            </span>
            <span className="hidden font-mono text-[12px] text-faint md:block">{it.family}</span>
            <span
              aria-hidden
              className="row-start-1 col-start-3 font-mono text-[14px] text-ink opacity-0 transition-[opacity,transform] duration-200 ease-[var(--ease-soft)] -translate-x-1 group-hover:translate-x-0 group-hover:opacity-100 group-focus-visible:translate-x-0 group-focus-visible:opacity-100 md:col-start-5"
            >
              →
            </span>
          </Link>
        ))}
        {shown.length === 0 && <p className="border-t border-line py-4 pl-3 font-mono text-[13px] text-faint">no match</p>}
      </div>
    </div>
  );
}
