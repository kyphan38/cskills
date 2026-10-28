'use client';

import { useEffect, useLayoutEffect, useRef, useState } from 'react';

// Table of contents beside a skill page. A 2px bar slides to the section
// you are reading, so you always know where you are on a long page.
export default function Toc({ items }: { items: { id: string; label: string }[] }) {
  const [active, setActive] = useState(0);
  const [bar, setBar] = useState<{ y: number; h: number } | null>(null);
  const refs = useRef<(HTMLAnchorElement | null)[]>([]);

  useEffect(() => {
    const heads = items.map((it) => document.getElementById(it.id)).filter((el): el is HTMLElement => !!el);
    const onScroll = () => {
      // The last heading above 35% of the screen is the one being read.
      const line = window.innerHeight * 0.35;
      let at = 0;
      heads.forEach((h, i) => {
        if (h.getBoundingClientRect().top < line) at = i;
      });
      const end = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
      setActive(end ? heads.length - 1 : at);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
    };
  }, [items]);

  useLayoutEffect(() => {
    const el = refs.current[active];
    if (el) setBar({ y: el.offsetTop, h: el.offsetHeight });
  }, [active]);

  if (items.length < 2) return null;

  return (
    <nav aria-label="on this page" className="relative border-l border-line">
      {bar && (
        <span
          aria-hidden
          className="absolute top-0 left-[-1px] w-[2px] bg-ink transition-transform duration-200 ease-[var(--ease-soft)]"
          style={{ transform: `translateY(${bar.y}px)`, height: bar.h }}
        />
      )}
      {items.map((it, i) => (
        <a
          key={it.id}
          ref={(el) => {
            refs.current[i] = el;
          }}
          href={`#${it.id}`}
          aria-current={i === active ? 'location' : undefined}
          className={`flex gap-2 py-1 pl-3 font-mono text-[12px] transition-colors ${i === active ? 'text-ink' : 'text-faint hover:text-muted'}`}
        >
          <span className="tabular-nums">{String(i + 1).padStart(2, '0')}</span>
          <span className="truncate">{it.label}</span>
        </a>
      ))}
    </nav>
  );
}
